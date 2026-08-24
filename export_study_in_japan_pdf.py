import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
HTML_PATH = BASE_DIR / "study_in_japan_guide_pdf.html"
OUTPUT_PDF = BASE_DIR / "generated_assets" / "Guia_Estudio_Visado_Universidad_Japon_Kamiyajuku.pdf"

async def generate_pdf():
    print("=" * 60)
    print("✈️ 神谷塾 公式『日本留学・ビザ・大学進学完全ガイド』PDF レンダリング")
    print("=" * 60)

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(f"file://{HTML_PATH.resolve()}", wait_until="networkidle")
        await page.wait_for_timeout(1000)

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
