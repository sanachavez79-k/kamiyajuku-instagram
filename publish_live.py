import os
from pathlib import Path
from integrations.instagram_api import InstagramAPIClient
from config import settings

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "generated_assets"

def publish_live_post():
    print("🚀 ========================================================")
    print("📸 神谷塾 (@japones_kamiyajuku) Instagram 本番自動投稿")
    print("🚀 ========================================================")

    client = InstagramAPIClient()

    # 1. 全6枚のスライド画像パスを取得
    slide_paths = [
        str(ASSETS_DIR / f"slide_{i}.jpg") for i in range(1, 7)
    ]
    
    for p in slide_paths:
        if not os.path.exists(p):
            raise FileNotFoundError(f"Slide image not found: {p}")

    print(f"📄 対象スライド: 全{len(slide_paths)}枚")
    for idx, p in enumerate(slide_paths, start=1):
        print(f"   Slide #{idx}: {Path(p).name}")

    # 2. Instagramキャプション本文
    caption = (
        "¿Alguna vez has dudado si usar 「に」 o 「で」 al hablar en japonés? 🤔🇯🇵\n\n"
        "En español usamos la palabra \"EN\" para casi todo: \"Vivo EN Tokio\" y \"Estudio EN Tokio\". "
        "Pero en japonés, ¡cometer este error te puede costar puntos muy valiosos en el examen JLPT (N5/N4)! ⚠️\n\n"
        "Desliza las imágenes para ver la regla y ponerte a prueba 📲👉\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📌 REGLA RÁPIDA DE REPASO:\n\n"
        "1️⃣ に (NI) ➔ Existencia, Estancia y Destino\n"
        "・東京に住んでいます (Vivo en Tokio)\n"
        "・机の上に猫がいます (Hay un gato sobre la mesa)\n\n"
        "2️⃣ で (DE) ➔ Acción activa\n"
        "・図書館で本を読みます (Leo libros en la biblioteca)\n"
        "・レストランで食べます (Como en un restaurante)\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "💬 ¡Ponte a prueba en los comentarios!\n"
        "¿Cómo se dice en japonés: \"Compré un libro EN Japón\"?\n"
        "A) 日本に本を買いました。\n"
        "B) 日本で本を買いました。\n\n"
        "¡Escribe tu respuesta abajo y te corregimos! 👇🎌\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🌸 ¿Quieres dominar el japonés y prepararte para viajar o estudiar en Japón?\n\n"
        "En Kamiyajuku (神谷塾) te ayudamos con clases online en vivo, profesores nativos certificados y asesoría para visas de estudio.\n\n"
        "📩 Envía un DM con la palabra \"JLPT\" y te enviaremos nuestra guía de estudio en PDF + un test diagnóstico gratuito.\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "#aprenderjapones #estudiarjapones #idiomajapones #nihongo #jlpt #jlptn5 #jlptn4 #examenjlpt #gramaticajaponesa #estudiarenjapon #viajarajapon #japonesonline #clasesdejapones #kamiyajuku #japon"
    )

    # 3. Instagramへ自動公開を実行
    print("\n📡 Instagram Graph APIへ送信中（画像アップロード ➔ カルーセル作成 ➔ 公開）...")
    result = client.publish_carousel_post(slide_paths, caption)

    print("\n🎉 ========================================================")
    print("✅ 投稿が完了しました！")
    print(f"   Published Media ID: {result.get('id')}")
    print("   Instagramアプリ（@japones_kamiyajuku）で最新の投稿をご確認ください！")
    print("🎉 ========================================================")
    return result

if __name__ == "__main__":
    publish_live_post()
