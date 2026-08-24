import os, sys, requests, json, time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from config import settings
from integrations.instagram_api import InstagramAPIClient
from render_master_carousel import DAY_CONFIGS

def main():
    c = DAY_CONFIGS["MIERCOLES"]
    slide_paths = [
        str(BASE_DIR / "generated_assets" / f"master_slide_MIERCOLES_{i}.jpg")
        for i in range(1, 7)
    ]

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

    ig = InstagramAPIClient()
    print("🚀 Instagram公式アカウントへ本番投稿を開始します...", flush=True)
    print(f"アカウントID: {ig.account_id}", flush=True)
    
    # 画像アップロード
    uploaded_urls = []
    for idx, img_path in enumerate(slide_paths, 1):
        print(f"[{idx}/6] スライド画像をアップロード中...", flush=True)
        url = ig.upload_local_image(img_path)
        print(f"    URL: {url}", flush=True)
        uploaded_urls.append(url)

    print("📦 カルーセル個別アイテムのコンテナを作成中...", flush=True)
    item_ids = []
    for idx, u in enumerate(uploaded_urls, 1):
        item_id = ig.create_carousel_item(u)
        print(f"    Item {idx} ID: {item_id}", flush=True)
        item_ids.append(item_id)

    print("📑 カルーセル親コンテナを作成中...", flush=True)
    container_id = ig.create_carousel_container(item_ids, caption)
    print(f"    Container ID: {container_id}", flush=True)

    time.sleep(3) # コンテナ準備待機

    print("🎉 Instagramへ本番公開中...", flush=True)
    publish_result = ig.publish_media(container_id)
    print("✨ 公開完了！", flush=True)
    print("Result:", json.dumps(publish_result, indent=2, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
