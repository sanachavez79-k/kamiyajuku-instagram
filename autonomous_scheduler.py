"""
Kamiya Juku Autonomous Instagram Scheduler (Cloud & Local Ready)
================================================================
1. Eve 21:00 CEST (Sun/Tue/Thu): Renders 6-slide carousel + caption and sends preview to Telegram.
   - Listens for interactive buttons (Schedule, Approve Now, Revise) with instant answerCallbackQuery.
   - Defaults to automatic publishing next day at 18:00 if no action taken (zero-stress guarantee).
2. Today 18:00 CEST (Mon/Wed/Fri): Automatically publishes approved carousel to Instagram (@japones_kamiyajuku).
3. 100% English file naming and full fallback support for content_ideas_sheet.xlsx.
"""

import os
import sys
import time
import json
import re
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from render_master_carousel import render_day_carousel, get_current_week_config, auto_add_furigana
from integrations.telegram_bot import TelegramNotificationClient
from integrations.instagram_api import InstagramAPIClient

MADRID_TZ = ZoneInfo("Europe/Madrid")

def get_madrid_now() -> datetime:
    """スペイン時間（Europe/Madrid）の現在日時を正確に取得"""
    return datetime.now(MADRID_TZ)

def clean_text_for_instagram(text: str) -> str:
    """HTMLタグ（ruby, span, b 等）を除去し、Instagram用の綺麗なプレーンテキストに変換"""
    if not text:
        return ""
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
        self.last_update_id = 0

    def generate_day_content_and_slides(self, day_key: str):
        """指定曜日のスライド画像全6枚とキャプションを生成"""
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

    def send_eve_preview(self, target_day_key: str, force: bool = False, wait_for_button: bool = True):
        """前日 12:00 にTelegramへプレビューと承認ボタンを送信し、ボタン押下を待機"""
        today_str = get_madrid_now().strftime("%Y-%m-%d")
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

        c = get_current_week_config(target_day_key)
        print(f"📡 前日12:00プレビューをTelegramへ配信中: 【{target_day_key}】 ({c['pillar']})")
        self.telegram.send_message(
            f"☀️ <b>【明日の投稿プレビュー】</b>\n\n"
            f"📌 テーマ: <b>{c['pillar']}</b>\n\n"
            f"以下のスライド全6枚とキャプションで、<b>明日 18:00（スペイン時間）にInstagram（@japones_kamiyajuku）へ自動公開</b>されます！🚀\n\n"
            f"💡 <b>【ご確認後の運用ガイド】</b>\n"
            f"・このままで問題なければ、<b>何も操作しなくても明日18:00に自動で公開</b>されます ✅\n"
            f"・今すぐ公開したい場合 ➔ [ ⚡️ 承認して今すぐ投稿 ]\n"
            f"・内容を変更したい場合 ➔ Google Driveの <code>02_planning/content_ideas_sheet.xlsx</code> を編集してください 📝"
        )
        self.telegram.send_preview_package(slide_paths, caption, post_id=post_id)
        print("✅ Telegram配信完了！")

        # 送信履歴を記録
        history[preview_key] = datetime.now().isoformat()
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

        # プレビュー送信後、最大10分間ボタン押下を待機（GitHub Actions / ローカル両対応）
        if wait_for_button:
            self.wait_for_user_action(timeout_seconds=600, expected_day=target_day_key)

        return slide_paths, caption, post_id

    def wait_for_user_action(self, timeout_seconds: int = 600, expected_day: str = "LUNES"):
        """ボタン押下をリアルタイム待機（最大timeout_seconds秒）。押されたら即座に応答してグルグルを解消"""
        print(f"⏳ Telegramボタン押下を待機中（最大 {timeout_seconds} 秒）...")
        start_time = time.time()
        import requests

        while time.time() - start_time < timeout_seconds:
            try:
                url = f"{self.telegram.base_url}/getUpdates"
                res = requests.get(url, params={"offset": self.last_update_id + 1, "timeout": 5}, timeout=10)
                data = res.json()
                if not data.get("ok"):
                    time.sleep(2)
                    continue

                for u in data.get("result", []):
                    self.last_update_id = u["update_id"]

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
                            self.telegram.send_message(
                                f"🎉 <b>【予約承認完了】</b>\n\n"
                                f"明日 18:00（スペイン時間）にInstagram公式アカウント（@japones_kamiyajuku）へ自動公開するよう予約しました！🚀✨"
                            )
                            print("🎉 承認完了を確認しました。")
                            return True

                        elif cb_data.startswith("APPROVE_NOW"):
                            self.telegram.send_message("🚀 <b>【即時公開処理中】</b> 公式Instagramへ投稿しています...")
                            self.publish_today_post(expected_day)
                            return True

                        elif cb_data.startswith("REVISE"):
                            self.telegram.send_message(
                                "📝 <b>【修正ガイド】</b>\n"
                                "Google Drive上の <code>content_ideas_sheet.xlsx</code> の該当行を編集して保存してください。\n"
                                "修正された内容で次回の生成・投稿が行われます！"
                            )
                            return True

            except Exception as e:
                pass

            time.sleep(2)

        print("⏰ 待機時間が終了しました。翌日18:00の自動スケジュールに移行します。")
        return False

    def publish_today_post(self, day_key: str):
        """当日 18:00 にInstagramへ投稿"""
        # 最新の未処理ボタン更新をすべてチェックして answerCallbackQuery
        self.poll_telegram_updates()

        slide_paths, caption = self.generate_day_content_and_slides(day_key)

        from render_master_carousel import mark_post_as_published, get_current_week_config
        c = get_current_week_config(day_key)
        row_id = c.get("_row_id")
        theme_name = c.get("pillar")

        print(f"🚀 Instagram公式アカウントへ本番投稿中: 【{day_key}】")
        pub_res = self.instagram.publish_carousel_post(slide_paths, caption)
        media_id = pub_res.get("id", pub_res.get("post_id", "N/A"))

        # 投稿完了後にキュー管理シートのステータスを published に自動更新
        mark_post_as_published(day_key=day_key, row_id=row_id, theme_name=theme_name)

        self.telegram.send_message(
            f"🎉 <b>【Instagram自動公開完了！】</b>\n\n"
            f"本日（{day_key}）のカルーセル投稿が正常に公開されました！✨\n"
            f"📌 テーマ: <b>{theme_name}</b>\n"
            f"🔗 <b>Media ID</b>: <code>{media_id}</code>\n"
            f"📱 Instagramアプリ（@japones_kamiyajuku）でご確認ください！"
        )

        return pub_res

    def poll_telegram_updates(self):
        """Telegramのボタン押下（callback_query）を処理してグルグルを解消"""
        import requests
        try:
            url = f"{self.telegram.base_url}/getUpdates"
            res = requests.get(url, params={"offset": self.last_update_id + 1, "timeout": 2}, timeout=5)
            data = res.json()
            if not data.get("ok"):
                return

            for u in data.get("result", []):
                self.last_update_id = u["update_id"]

                if "callback_query" in u:
                    cb = u["callback_query"]
                    cb_id = cb.get("id")
                    requests.post(
                        f"{self.telegram.base_url}/answerCallbackQuery",
                        json={"callback_query_id": cb_id, "text": "✅ 受付完了しました！"}
                    )
        except Exception:
            pass

    def run_check_cycle(self):
        """現在時刻を判定して前夜21:00通知または当日18:00投稿を実行"""
        now = get_madrid_now()
        weekday = now.weekday() # 0: Mon, 1: Tue, 2: Wed, 3: Thu, 4: Fri, 5: Sat, 6: Sun
        hour = now.hour
        today_str = now.strftime("%Y-%m-%d")

        eve_mapping = {
            6: "LUNES",     # 日曜 21:00 -> 月曜分
            1: "MIERCOLES", # 火曜 21:00 -> 水曜分
            3: "VIERNES"    # 木曜 21:00 -> 金曜分
        }

        today_mapping = {
            0: "LUNES",     # 月曜 18:00
            2: "MIERCOLES", # 水曜 18:00
            4: "VIERNES"    # 金曜 18:00
        }

        history_file = BASE_DIR / "scheduler_history.json"
        history = {}
        if history_file.exists():
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass

        if weekday in eve_mapping:
            target_day = eve_mapping[weekday]
            preview_key = f"preview_{today_str}_{target_day}"
            if hour >= 12 and not history.get(preview_key):
                print(f"⏰ 前日12:00プレビュー配信トリガー検知: 翌日【{target_day}】分を配信します")
                self.send_eve_preview(target_day)

        if weekday in today_mapping:
            target_day = today_mapping[weekday]
            publish_key = f"publish_{today_str}_{target_day}"
            if hour >= 18 and not history.get(publish_key):
                print(f"⏰ 当日18:00投稿トリガー検知: 本日【{target_day}】分を投稿します")
                self.publish_today_post(target_day)
                history[publish_key] = datetime.now().isoformat()
                with open(history_file, "w", encoding="utf-8") as f:
                    json.dump(history, f, indent=2)

    def run_forever(self):
        """完全自律監視ループ"""
        print("🤖 神谷塾 自律型スケジューラーが稼働開始しました（常駐監視中）...", flush=True)

        last_check_min = -1
        while True:
            try:
                self.poll_telegram_updates()
                current_min = get_madrid_now().minute
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
                weekday = get_madrid_now().weekday()
                eve_map = {6: "LUNES", 1: "MIERCOLES", 3: "VIERNES"}
                day = eve_map.get(weekday, "MIERCOLES")
            # GitHub Actions実行時は wait_for_button=True (最大10分待機)
            scheduler.send_eve_preview(day, force=True, wait_for_button=True)
        elif cmd in ["publish", "publish_today"]:
            if len(sys.argv) > 2:
                day = sys.argv[2].upper()
            else:
                weekday = get_madrid_now().weekday()
                today_map = {0: "LUNES", 2: "MIERCOLES", 4: "VIERNES"}
                day = today_map.get(weekday, "LUNES")
            scheduler.publish_today_post(day)
        elif cmd in ["daemon", "start"]:
            scheduler.run_forever()
    else:
        scheduler.run_check_cycle()
