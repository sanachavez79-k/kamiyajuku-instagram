import os
import sys
import time
import asyncio
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from render_master_carousel import DAY_CONFIGS, render_day_carousel
from integrations.telegram_bot import TelegramNotificationClient
from integrations.instagram_api import InstagramAPIClient

def main():
    day_key = "MIERCOLES"
    c = DAY_CONFIGS[day_key]
    telegram = TelegramNotificationClient()

    if not telegram.is_configured():
        print("❌ TelegramのトークンまたはChat IDが設定されていません。")
        return

    print("🚀 スライド全6枚とキャプションを準備中...", flush=True)
    slide_paths = [
        str(BASE_DIR / "generated_assets" / f"master_slide_MIERCOLES_{i}.jpg")
        for i in range(1, 7)
    ]
    # ファイルが存在しない場合のみレンダリング
    if not all(os.path.exists(p) for p in slide_paths):
        slide_paths = asyncio.run(render_day_carousel(day_key))

    caption = (
        f"⛩️ Kamiya Juku | {c['tag_text']}\n\n"
        f"📌 {c['subtitle']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"1️⃣ {c['rule1']['badge']}: {c['rule1']['title']}\n"
        f"   👉 {c['rule1']['desc']}\n\n"
        f"2️⃣ {c['rule2']['badge']}: {c['rule2']['title']}\n"
        f"   👉 {c['rule2']['desc']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"✍️ ¡Desliza hasta el final para poner a prueba tu japonés con el mini quiz!\n\n"
        f"🎁 【REGALO GRATUITO】\n"
        f"Envía un mensaje directo (DM) con la palabra \"{c['dm_keyword']}\" y te enviaremos nuestra {c['dm_gift'].replace('<b>','').replace('</b>','')}.\n\n"
        f"✨ ¡Aprende con profesores nativos y cumple tu sueño de estudiar o trabajar en Japón!\n"
        f"📱 WhatsApp: +34 682 054 654\n"
        f"✉️ Email: info@kamiyajuku.com\n\n"
        f"#aprenderjapones #estudiarjapones #nihongo #jlpt #kamiyajuku #japon #barcelona #clasesdejapones #estudiarenjapon"
    )

    post_id = f"MIERCOLES_{int(time.time())}"

    print(f"📡 Telegramへプレビュー送信中...")
    telegram.send_message(
        "⛩️ *【神谷塾】水曜日の最新投稿プレビューをお届けします！*\n"
        "テーマ: 『すみません vs ごめん』\n\n"
        "以下のスライド（全6枚）とキャプションをご確認いただき、問題なければ **「🚀 承認してInstagramに投稿」** ボタンを押してください！押した瞬間に即時公開されます。"
    )
    telegram.send_preview_package(slide_paths, caption, post_id=post_id)
    print("✅ Telegramへのプレビュー送信が完了しました！")

    # 承認待機リスナーの開始
    print("🤖 承認ボタンの待機中...")
    telegram.listen_and_handle_interactive_session(
        pipeline_runner=None,
        day_key=day_key,
        current_topic_data=c,
        slide_paths=slide_paths,
        caption=caption,
        post_id=post_id
    )

if __name__ == "__main__":
    main()
