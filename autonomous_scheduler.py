"""
神谷塾 完全自律型 Instagram 運用スケジューラー (Autonomous Scheduler)
======================================================
1. 投稿前夜 21:00 (日・火・木) に翌日分のカルーセル（全6枚）＋キャプションを生成しTelegramへ通知。
2. ユーザーはスマホからボタン1つで「承認」または「修正指示」。
3. 投稿当日 18:00 (月・水・金) にInstagramへ公式自動投稿。
4. テーマと生徒写真の自動切替:
   - 月曜: JLPT文法・重要助詞 (抹茶パステル + 留学生集合写真)
   - 水曜: 日常会話・リアル表現 (マスタードパステル + 祭り交流写真)
   - 金曜: 日本留学・ビザ・文化 (ミントパステル + HOKKAIDO授業写真)
"""

import os
import sys
import time
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from render_master_carousel import render_day_carousel, get_current_week_config
from integrations.telegram_bot import TelegramNotificationClient
from integrations.instagram_api import InstagramAPIClient

def clean_text_for_instagram(text: str) -> str:
    """HTMLタグ（ruby, span, b 等）を除去し、Instagram用の綺麗なプレーンテキストに変換"""
    if not text:
        return ""
    import re
    # ruby タグ: <ruby>雨<rt>あめ</rt></ruby> -> 雨
    t = re.sub(r'<ruby>([^<]+)<rt>[^<]*</rt></ruby>', r'\1', text)
    # 残りのHTMLタグ除去
    t = re.sub(r'<[^>]+>', '', t)
    # 特殊文字
    t = t.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return t.strip()

class KamiyajukuAutonomousScheduler:
    def __init__(self):
        self.telegram = TelegramNotificationClient()
        self.instagram = InstagramAPIClient()
        self.assets_dir = BASE_DIR / "generated_assets"
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def generate_day_content_and_slides(self, day_key: str):
        """指定曜日のスライド画像全6枚とキャプションを生成"""
        from render_master_carousel import get_current_week_config
        c = get_current_week_config(day_key)
        print(f"\n🚀 【{day_key}】 スライド全6枚のレンダリング開始... (テーマ: {c['pillar']})")
        slide_paths = asyncio.run(render_day_carousel(day_key))

        r1_desc = clean_text_for_instagram(c['rule1']['desc'])
        r1_ja = clean_text_for_instagram(c['rule1']['ja'])
        r1_es = clean_text_for_instagram(c['rule1']['es'])

        r2_desc = clean_text_for_instagram(c['rule2']['desc'])
        r2_ja = clean_text_for_instagram(c['rule2']['ja'])
        r2_es = clean_text_for_instagram(c['rule2']['es'])

        dm_gift = clean_text_for_instagram(c['dm_gift'])
        subtitle = clean_text_for_instagram(c['subtitle'])
        tag_text = clean_text_for_instagram(c['tag_text'])

        caption = (
            f"⛩️ Kamiya Juku | {tag_text}\n\n"
            f"📌 {subtitle}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ {c['rule1']['badge']}: {c['rule1']['title']}\n"
            f"   👉 {r1_desc}\n"
            f"   ・{r1_ja} ({r1_es})\n\n"
            f"2️⃣ {c['rule2']['badge']}: {c['rule2']['title']}\n"
            f"   👉 {r2_desc}\n"
            f"   ・{r2_ja} ({r2_es})\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"✍️ ¡Desliza hasta el final para poner a prueba tu japonés con el mini quiz!\n\n"
            f"🎁 【REGALO GRATUITO】\n"
            f"Envía un mensaje directo (DM) con la palabra \"{c['dm_keyword']}\" y te enviaremos nuestra {dm_gift}.\n\n"
            f"✨ ¡Aprende con profesores nativos y cumple tu sueño de estudiar o trabajar en Japón!\n"
            f"📱 WhatsApp: +34 682 054 654\n"
            f"✉️ Email: info@kamiyajuku.com\n\n"
            f"#aprenderjapones #estudiarjapones #nihongo #jlpt #kamiyajuku #japon #barcelona #clasesdejapones #estudiarenjapon"
        )

        return slide_paths, caption

    def send_eve_preview(self, target_day_key: str, force: bool = False):
        """前夜 21:00 にTelegramへプレビューと承認ボタンを送信（重複防止ロック付き）"""
        today_str = datetime.now().strftime("%Y-%m-%d")
        history_file = BASE_DIR / "scheduler_history.json"
        history = {}
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass

        preview_key = f"preview_{today_str}_{target_day_key}"
        if not force and history.get(preview_key):
            print(f"ℹ️ 本日分のプレビュー（{target_day_key}）は既に送信済みです（重複送信をスキップ）。")
            return [], "", ""

        slide_paths, caption = self.generate_day_content_and_slides(target_day_key)
        post_id = f"{target_day_key}_{int(time.time())}"

        from render_master_carousel import get_current_week_config
        c = get_current_week_config(target_day_key)
        print(f"📡 前夜プレビューをTelegramへ配信中: 【{target_day_key}】 ({c['pillar']})")
        self.telegram.send_message(
            f"🌙 *【明日の投稿プレビュー】*\n"
            f"明日（{c['pillar']}）の投稿案が完成しました！\n"
            f"スライド画像全6枚とキャプションを確認して「承認」または「修正」を押してください。"
        )
        self.telegram.send_preview_package(slide_paths, caption, post_id=post_id)
        print("✅ Telegram配信完了！")

        # 送信履歴を記録
        history[preview_key] = datetime.now().isoformat()
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

        return slide_paths, caption, post_id

    def publish_today_post(self, day_key: str):
        """当日 18:00 にInstagramへ投稿"""
        schedule_file = BASE_DIR / "approved_schedule.json"
        
        # 承認済みスケジュールがある場合はそれを使用
        if schedule_file.exists():
            try:
                with open(schedule_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                slide_paths = data.get("slides", [])
                caption = data.get("caption", "")
                day_key = data.get("day_key", day_key)
                print(f"📦 承認済みスケジュールデータを読み込みました: 【{day_key}】")
            except Exception as e:
                print(f"⚠️ スケジュールファイル読み込みエラー: {e}")
                slide_paths, caption = self.generate_day_content_and_slides(day_key)
        else:
            slide_paths, caption = self.generate_day_content_and_slides(day_key)

        print(f"🚀 Instagram公式アカウントへ本番投稿中: 【{day_key}】")
        pub_res = self.instagram.publish_carousel_post(slide_paths, caption)
        media_id = pub_res.get("id", pub_res.get("post_id", "N/A"))

        self.telegram.send_message(
            f"🎉 <b>【Instagram自動公開完了！】</b>\n\n"
            f"本日（{day_key}）のカルーセル投稿が正常に公開されました！✨\n"
            f"🔗 <b>Media ID</b>: <code>{media_id}</code>\n"
            f"📱 Instagramアプリでご確認ください！"
        )

        # 投稿完了後にスケジュールファイルを削除
        if schedule_file.exists():
            schedule_file.unlink(missing_ok=True)

        return pub_res

    def run_check_cycle(self):
        """現在時刻を判定して前夜21:00通知または当日18:00投稿を実行（スリープ復帰時のキャッチアップ対応）"""
        now = datetime.now()
        weekday = now.weekday() # 0: Mon, 1: Tue, 2: Wed, 3: Thu, 4: Fri, 5: Sat, 6: Sun
        hour = now.hour
        today_str = now.strftime("%Y-%m-%d")

        eve_mapping = {
            6: "LUNES",     # 日曜 -> 月曜分
            1: "MIERCOLES", # 火曜 -> 水曜分
            3: "VIERNES"    # 木曜 -> 金曜分
        }

        today_mapping = {
            0: "LUNES",     # 月曜
            2: "MIERCOLES", # 水曜
            4: "VIERNES"    # 金曜
        }

        history_file = BASE_DIR / "scheduler_history.json"
        history = {}
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass

        # 1. 前夜プレビュー判定（21:00〜翌日未明にかけて未送信なら送信）
        if weekday in eve_mapping:
            target_day = eve_mapping[weekday]
            preview_key = f"preview_{today_str}_{target_day}"
            # 21時以降、またはスリープ復帰で21時〜23時の間に未送信だった場合
            if hour >= 21 and not history.get(preview_key):
                print(f"⏰ 前夜プレビュー配信トリガー検知: 翌日【{target_day}】分を配信します")
                self.send_eve_preview(target_day)

        # 2. 当日本番投稿判定（18:00以降に未投稿なら投稿）
        if weekday in today_mapping:
            target_day = today_mapping[weekday]
            publish_key = f"publish_{today_str}_{target_day}"
            if hour >= 18 and not history.get(publish_key):
                print(f"⏰ 当日投稿トリガー検知: 本日【{target_day}】分を投稿します")
                self.publish_today_post(target_day)
                history[publish_key] = datetime.now().isoformat()
                with open(history_file, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=2)

    def poll_telegram_updates(self):
        """Telegramのボタン押下（callback_query）やメッセージをリアルタイム処理し、グルグルを即座に解消"""
        import requests
        if not hasattr(self, "last_update_id"):
            self.last_update_id = 0

        try:
            url = f"{self.telegram.base_url}/getUpdates"
            res = requests.get(url, params={"offset": self.last_update_id + 1, "timeout": 2}, timeout=5)
            data = res.json()
            if not data.get("ok"):
                return

            for u in data.get("result", []):
                self.last_update_id = u["update_id"]

                # 1. インラインボタン押下時
                if "callback_query" in u:
                    cb = u["callback_query"]
                    cb_data = cb.get("data", "")
                    cb_id = cb.get("id")

                    # 即座にグルグルを止める
                    requests.post(
                        f"{self.telegram.base_url}/answerCallbackQuery",
                        json={"callback_query_id": cb_id, "text": "✅ 受付完了しました！"}
                    )

                    print(f"📲 Telegramボタン押下検知: {cb_data}")

                    if cb_data.startswith("SCHEDULE"):
                        # 明日18:00の予約保存
                        parts = cb_data.split("_")
                        day_key = parts[1] if len(parts) > 1 else "LUNES"
                        slide_paths, caption = self.generate_day_content_and_slides(day_key)
                        
                        schedule_file = BASE_DIR / "approved_schedule.json"
                        with open(schedule_file, "w", encoding="utf-8") as f:
                            json.dump({
                                "day_key": day_key,
                                "slides": slide_paths,
                                "caption": caption,
                                "approved": True,
                                "scheduled_time": "18:00"
                            }, f, ensure_ascii=False, indent=2)

                        self.telegram.send_message(
                            f"🎉 <b>【承認完了】</b>\n\n"
                            f"明日（18:00 スペイン時間）にInstagram公式アカウント（@japones_kamiyajuku）へ自動公開するよう予約完了しました！🚀✨\n\n"
                            f"（※明日18:00に公開完了通知をお届けします）"
                        )
                        print("🎉 承認完了！明日18:00投稿として保存しました。")

                    elif cb_data.startswith("APPROVE_NOW"):
                        parts = cb_data.split("_")
                        day_key = parts[2] if len(parts) > 2 else "LUNES"
                        self.telegram.send_message("🚀 <b>【即時公開処理中】</b> 公式Instagramへ投稿しています...")
                        self.publish_today_post(day_key)

                    elif cb_data.startswith("REVISE"):
                        self.telegram.send_message(
                            "✍️ <b>【修正受付】</b>\n変更したい箇所（例: 『タイトルを〜にして』『例文を〜に変えて』）をこのチャットにそのまま返信してください！"
                        )

                # 2. テキストメッセージ受信時
                elif "message" in u and "text" in u["message"]:
                    msg_text = u["message"]["text"].strip()
                    msg_id = u["message"]["message_id"]
                    print(f"💬 Telegramメッセージ受信: {msg_text}")

        except Exception as e:
            # タイムアウト等の軽微なエラーは無視
            pass

    def run_forever(self):
        """完全自律監視ループ（スケジュール判定 ＋ リアルタイムTelegramリスナー）"""
        print("🤖 神谷塾 自律型スケジューラーが稼働開始しました（常駐監視中）...", flush=True)

        last_check_min = -1
        while True:
            try:
                # 1. Telegramボタン押下を即座に処理（グルグル防止）
                self.poll_telegram_updates()

                # 2. スケジュール判定（1分に1回）
                current_min = datetime.now().minute
                if current_min != last_check_min:
                    last_check_min = current_min
                    self.run_check_cycle()

            except Exception as e:
                print(f"⚠️ スケジューラーループ内エラー: {e}")

            time.sleep(2)

if __name__ == "__main__":
    scheduler = KamiyajukuAutonomousScheduler()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ["preview", "eve_preview"]:
            if len(sys.argv) > 2:
                day = sys.argv[2].upper()
            else:
                weekday = datetime.now().weekday()
                eve_map = {6: "LUNES", 1: "MIERCOLES", 3: "VIERNES"}
                day = eve_map.get(weekday, "LUNES")
            scheduler.send_eve_preview(day, force=True)
        elif cmd in ["publish", "publish_today"]:
            if len(sys.argv) > 2:
                day = sys.argv[2].upper()
            else:
                weekday = datetime.now().weekday()
                today_map = {0: "LUNES", 2: "MIERCOLES", 4: "VIERNES"}
                day = today_map.get(weekday, "LUNES")
            scheduler.publish_today_post(day)
        elif cmd in ["daemon", "start"]:
            scheduler.run_forever()
    else:
        scheduler.run_check_cycle()
