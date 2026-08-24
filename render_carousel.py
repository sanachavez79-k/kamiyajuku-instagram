import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "carousel_template.html"
OUTPUT_DIR = BASE_DIR / "generated_assets"
OUTPUT_DIR.mkdir(exist_ok=True)

def render_slides_with_chrome():
    """
    Chrome / Edge のヘッドレスモードまたはスクリプトを使用して
    HTML内の5つのスライド（1080x1350）を個別の高解像度画像に出力するレンダラー
    """
    print(f"🎨 Rendering carousel slides from {HTML_FILE}...")

    # macOSにインストールされているGoogle Chromeのパスを検索
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    ]
    
    browser_bin = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser_bin = p
            break

    if not browser_bin:
        print("⚠️ Chrome browser not found directly. You can open 'carousel_template.html' in your browser to inspect or export.")
        return False

    # ヘッドレスChromeで1080x1350解像度でスクリーンショット取得
    cmd = [
        browser_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        f"--window-size=1080,7200",
        f"--screenshot={OUTPUT_DIR / 'full_carousel_preview.png'}",
        f"file://{HTML_FILE}"
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Full preview generated: {OUTPUT_DIR / 'full_carousel_preview.png'}")
    return True

if __name__ == "__main__":
    render_slides_with_chrome()
