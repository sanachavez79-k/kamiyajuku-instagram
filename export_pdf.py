import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
HTML_PATH = BASE_DIR / "study_guide_pdf.html"
OUTPUT_PDF = BASE_DIR / "generated_assets" / "Guia_Definitiva_Particulas_JLPT_Kamiyajuku.pdf"

async def generate_pdf():
    print("=" * 60)
    print("📚 神谷塾 公式PDF学習ガイド教材 レンダリング生成")
    print("=" * 60)

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # HTMLを読み込み
        await page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # A4 PDFとして出力
        await page.pdf(
            path=str(OUTPUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )

        await browser.close()

    print(f"✅ PDF生成完了: {OUTPUT_PDF}")
    print(f"   ファイルサイズ: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
