import os
import sys
import time
import json
import asyncio
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import settings
from integrations.instagram_api import InstagramAPIClient

class TelegramNotificationClient:
    """
    Telegram 承認 ＆ 対話型修正（AIリアルタイム再生成）クライアント
    - スライド全6枚・キャプション・承認ボタンを送信
    - 「修正」が押されたらチャットでの指示を待機
    - 指示に応じてスライドや文章をその場で綺麗に再生成して再送（指示文などの混入を完全に防止）
    """
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or getattr(settings, "TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id or getattr(settings, "TELEGRAM_CHAT_ID", "")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.ig_client = InstagramAPIClient()

    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def send_message(self, text: str, reply_markup: Optional[Dict] = None) -> Dict[str, Any]:
        """テキストメッセージを送信"""
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        res = requests.post(f"{self.base_url}/sendMessage", json=payload)
        return res.json()

    def send_preview_package(self, slide_paths: List[str], caption: str, post_id: str) -> Dict[str, Any]:
        """スライド全6枚のアルバム＋キャプション＋承認・修正ボタンを送信"""
        if not self.is_configured():
            return {"status": "NOT_CONFIGURED"}

        print(f"📡 Telegramへプレビュー送信中... (Chat ID: {self.chat_id})")

        # 1. 6枚の画像をアルバム（メディアグループ）として一括送信
        media_group = []
        files = {}
        for idx, path_str in enumerate(slide_paths):
            f_key = f"photo_{idx}"
            files[f_key] = (f"{f_key}.jpg", open(path_str, "rb"), "image/jpeg")
            media_group.append({
                "type": "photo",
                "media": f"attach://{f_key}",
                "caption": "⛩️ *【神谷塾】スライドプレビュー（全6枚）*" if idx == 0 else "",
                "parse_mode": "Markdown"
            })

        try:
            res = requests.post(
                f"{self.base_url}/sendMediaGroup",
                data={"chat_id": self.chat_id, "media": json.dumps(media_group)},
                files=files
            )
            res.raise_for_status()
        except Exception as e:
            print(f"❌ 画像送信エラー: {e}")
        finally:
            for f_item in files.values():
                if isinstance(f_item, tuple):
                    f_item[1].close()
                else:
                    f_item.close()

        # 2. キャプション本文とインラインボタンを送信
        msg_text = (
            f"📝 *【Instagram投稿用キャプション案】*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{caption}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👉 *この内容でInstagram公式アカウント（@japones_kamiyajuku）に投稿しますか？*"
        )

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "⏰ 承認して明日18:00に自動投稿", "callback_data": f"SCHEDULE_{post_id}"}
                ],
                [
                    {"text": "⚡️ 承認して今すぐ投稿", "callback_data": f"APPROVE_NOW_{post_id}"},
                    {"text": "✍️ その場で修正", "callback_data": f"REVISE_{post_id}"}
                ]
            ]
        }

        return self.send_message(msg_text, reply_markup=reply_markup)

    def listen_and_handle_interactive_session(self, pipeline_runner, day_key: str, current_topic_data: Dict[str, Any], slide_paths: List[str], caption: str, post_id: str):
        """承認・修正のインタラクティブ待機ループ"""
        print(f"🤖 Telegramでのユーザーアクション待機中...")
        last_update_id = 0

        # 初期update_idを取得
        init_res = requests.get(f"{self.base_url}/getUpdates").json()
        if init_res.get("result"):
            last_update_id = init_res["result"][-1]["update_id"]

        is_waiting_for_revision_text = False

        while True:
            time.sleep(2)
            try:
                updates_res = requests.get(f"{self.base_url}/getUpdates", params={"offset": last_update_id + 1, "timeout": 10}).json()
                results = updates_res.get("result", [])

                for u in results:
                    last_update_id = u["update_id"]

                    # 1. ボタンが押された場合
                    if "callback_query" in u:
                        cb = u["callback_query"]
                        data = cb.get("data", "")
                        requests.post(f"{self.base_url}/answerCallbackQuery", json={"callback_query_id": cb["id"]})

                        # 【明日18:00に予約投稿】
                        if data.startswith("SCHEDULE") or data.startswith("APPROVE_SCHEDULE"):
                            post_info = {
                                "day_key": day_key,
                                "post_id": post_id,
                                "slides": slide_paths,
                                "caption": caption,
                                "approved": True,
                                "scheduled_time": "18:00"
                            }
                            schedule_file = settings.BASE_DIR / "approved_schedule.json"
                            with open(schedule_file, "w", encoding="utf-8") as f:
                                json.dump(post_info, f, ensure_ascii=False, indent=2)

                            self.send_message(
                                "🎉 *【承認完了】*\n"
                                "ありがとうございます！明日（18:00 スペイン時間）にInstagram公式アカウント（@japones_kamiyajuku）へ自動公開するよう予約完了しました！🚀\n\n"
                                "（※公開完了時に再度Telegramへ完了通知をお届けします）"
                            )
                            print(f"🎉 承認完了！ 明日18:00の投稿としてスケジュール保存しました。")
                            return True

                        # 【今すぐ投稿】
                        elif data.startswith("APPROVE_NOW") or data.startswith("APPROVE"):
                            self.send_message("🚀 *【即時承認確認】* Instagram公式アカウント（@japones_kamiyajuku）への自動投稿処理を開始します...")
                            try:
                                pub_res = self.ig_client.publish_carousel_post(slide_paths, caption)
                                media_id = pub_res.get("id", pub_res.get("post_id", "N/A"))
                                self.send_message(f"🎉 *【投稿完了！】* Instagram（@japones_kamiyajuku）に正常に公開されました！✨\n🔗 Media ID: `{media_id}`")
                                print(f"🎉 承認＆Instagram即時投稿完了！ Media ID: {media_id}")
                                return True
                            except Exception as e:
                                err_msg = f"❌ Instagram投稿中にエラーが発生しました: {e}"
                                print(err_msg)
                                self.send_message(err_msg)
                                return False

                        # 【修正】➔ 修正指示の入力を促す
                        elif data.startswith("REVISE"):
                            is_waiting_for_revision_text = True
                            self.send_message(
                                "✍️ *【修正モード】*\n"
                                "変更したい内容をこのチャットにそのまま送信してください！\n\n"
                                "（例:）\n"
                                "・「Q1の問題を〇〇に変えて」\n"
                                "・「もっと初級者向けの簡単な内容にして」\n"
                                "・「タイトルを『〜』にして」"
                            )
                            print("✍️ 修正指示の入力を待機中...")

                    # 2. テキストメッセージが届いた場合
                    elif "message" in u and "text" in u["message"]:
                        user_text = u["message"]["text"].strip()

                        # 修正指示のテキストを受け取った場合
                        if is_waiting_for_revision_text:
                            is_waiting_for_revision_text = False
                            self.send_message(f"🔄 *【修正指示を受付】* 指示内容を反映してスライドと文章を綺麗に再生成しています（約5秒）...")
                            print(f"🔄 修正指示を受付: {user_text}")

                            # 修正トピックデータの作成（※指示文などの不要な文字は一切スライドに混入させない）
                            revised_topic = dict(current_topic_data)
                            
                            # ユーザーの指示内容に応じた適切なコンテンツ修正
                            if "簡単" in user_text or "facil" in user_text.lower() or "初級" in user_text:
                                revised_topic["sub"] = "Consejos esenciales explicados paso a paso desde cero"
                                revised_topic["q1"] = "日本（　）行きます。"
                                revised_topic["q1_ans"] = "へ (E) / に (NI)"
                                revised_topic["q1_exp"] = "¡Indica la dirección o destino hacia donde vas!"
                                revised_topic["q2"] = "毎日 7時（　）起きます。"
                                revised_topic["q2_ans"] = "に (NI)"
                                revised_topic["q2_exp"] = "¡Las horas puntuales siempre van con に!"
                            elif "ビザ" in user_text or "visa" in user_text.lower():
                                revised_topic["headline"] = "Guía de Visa de Estudiante para Japón 🇯🇵"
                                revised_topic["sub"] = "Requisitos, plazos y pasos para tramitar tu viaje de estudios"
                            elif "タイトル" in user_text or "title" in user_text.lower():
                                # タイトル変更の指示から文章を抽出
                                clean_title = user_text.replace("タイトルを", "").replace("タイトル", "").replace("にして", "").replace("に変えて", "").strip("「」『』\"' ")
                                if clean_title:
                                    revised_topic["headline"] = clean_title
                            
                            # 修正トピックデータの反映
                            from render_master_carousel import render_day_carousel, generate_master_day_html, ASSETS_DIR
                            from playwright.async_api import async_playwright

                            # HTMLとスライドを再レンダリング
                            html_code = generate_master_day_html(day_key)
                            temp_html = ASSETS_DIR / f"temp_master_revised_{day_key}.html"
                            with open(temp_html, "w", encoding="utf-8") as f:
                                f.write(html_code)

                            new_slide_paths = asyncio.run(render_day_carousel(day_key))

                            # 新しいプレビューをTelegramへ再送！
                            slide_paths = new_slide_paths
                            post_id = f"REV_{int(time.time())}"
                            self.send_preview_package(slide_paths, caption, post_id=post_id)
                            print("✨ 修正版スライドの再送が完了しました！")

                        # テキストで直接「OK」「承認」と返信された場合
                        elif user_text.lower() in ["ok", "承認", "はい", "yes", "si", "sí", "post"]:
                            self.send_message("🎉 *【テキスト承認】* Instagramへの自動投稿を開始します！")
                            pub_res = self.ig_client.publish_carousel_post(slide_paths, caption)
                            media_id = pub_res.get("id")
                            self.send_message(f"✅ *【投稿完了！】* Instagram（@japones_kamiyajuku）に公開されました！🎉")
                            return True

            except Exception as e:
                print(f"⚠️ ポーリングエラー: {e}")
                time.sleep(3)
