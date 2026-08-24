import os
import sys
import time
from datetime import datetime
from automation_pipeline import FullAutomationPipeline

def get_current_day_key() -> str:
    weekday = datetime.now().weekday()
    # 0: Monday, 2: Wednesday, 4: Friday
    mapping = {
        0: "LUNES",
        2: "MIERCOLES",
        4: "VIERNES"
    }
    return mapping.get(weekday, None)

def run_weekly_scheduler():
    print("=" * 60)
    print("🤖 神谷塾 Instagram 週3回自動運用スケジューラー稼働中")
    print("   投稿スケジュール: 毎週 月曜・水曜・金曜 18:00 (スペイン時間)")
    print("=" * 60)

    pipeline = FullAutomationPipeline()

    day_key = get_current_day_key()
    if not day_key:
        print(f"ℹ️ 本日は投稿対象曜日（月・水・金）ではありません。(現在: {datetime.now().strftime('%A')})")
        return

    print(f"⏰ 投稿対象曜日です: 【{day_key}】")
    # 本番自動投稿を実行
    pipeline.run_pipeline(day_key, publish_live=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].upper() in ["LUNES", "MIERCOLES", "VIERNES"]:
        manual_day = sys.argv[1].upper()
        pipeline = FullAutomationPipeline()
        pipeline.run_pipeline(manual_day, publish_live="--publish" in sys.argv)
    else:
        run_weekly_scheduler()
