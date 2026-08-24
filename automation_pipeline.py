"""
神谷塾 完全自動化パイプライン (Master Automation Pipeline)
- お気に入りの「大文字・ふりがな・対比カード・生徒写真・WhatsApp連絡先付きCTA」をベースに統一。
- 曜日ごとのパステルカラー（月：抹茶、水：マスタード、金：ミント）を適用。
- Telegram送信はユーザー指示に従いデフォルトOFF（ローカル保存・確認優先）。
"""

import os
import sys
import asyncio
from pathlib import Path
from render_master_carousel import render_all_master_slides, DAY_STYLES

class MasterAutomationPipeline:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.assets_dir = self.base_dir / "generated_assets"
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def run(self, day_key="LUNES"):
        style = DAY_STYLES.get(day_key, DAY_STYLES["LUNES"])
        print(f"\n🎨 神谷塾 カルーセル生成開始: 【{day_key}】 {style['name']}")
        slides = asyncio.run(render_all_master_slides(day_key))
        print(f"✅ 全 {len(slides)} 枚のスライド生成完了！")
        return slides

if __name__ == "__main__":
    day = sys.argv[1] if len(sys.argv) > 1 else "LUNES"
    pipeline = MasterAutomationPipeline()
    pipeline.run(day)
