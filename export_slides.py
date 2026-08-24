import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "carousel_template.html"
OUTPUT_DIR = BASE_DIR / "generated_assets"
OUTPUT_DIR.mkdir(exist_ok=True)

def export_with_playwright():
    """
    Playwright を使用して HTML テンプレートから 6枚のスライドを
    Instagram推奨の 1080x1350 高解像度 JPG 画像に自動書き出しするスクリプト
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("💡 Playwright がインストールされていません。")
        print("   自動書き出しを利用する場合は、以下を実行してください:")
        print("   pip install playwright && playwright install chromium\n")
        print("👉 または、ブラウザで 'carousel_template.html' を開いて")
        print("   画面上部の「📸 全スライドを一括JPG保存」ボタンをクリックすれば、今すぐ6枚保存できます！")
        return

    print("🚀 Playwright を起動してスライド画像を生成中...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 高解像度デバイススケール 2x (2160 x 2700) でRetina品質のJPGを出力
        context = browser.new_context(
            viewport={"width": 1200, "height": 9000},
            device_scale_factor=2
        )
        page = context.new_page()
        page.goto(f"file://{HTML_FILE}", wait_until="networkidle")

        slides = page.query_selector_all(".slide")
        print(f"📄 見つかったスライド数: {len(slides)} 枚")

        for idx, slide in enumerate(slides, start=1):
            out_path = OUTPUT_DIR / f"slide_{idx}.jpg"
            slide.screenshot(path=str(out_path), type="jpeg", quality=95)
            print(f"   ✅ [Slide {idx}/6] 保存完了 ➔ {out_path.name}")

        browser.close()

    print(f"\n🎉 すべてのスライド（全6枚）が '{OUTPUT_DIR.name}/' に出力されました！")

if __name__ == "__main__":
    export_with_playwright()
