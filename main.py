import argparse
import json
from agents.supervisor import SupervisorAgent
from schemas import PostStatus

def main():
    parser = argparse.ArgumentParser(description="Kamiyajuku Instagram Multi-Agent Pipeline Runner")
    parser.add_argument("--theme", type=str, default=None, help="Specific topic or grammar point")
    parser.add_argument("--story", action="store_true", help="Post as Instagram Story using Drive asset")
    parser.add_argument("--simulate-approval", action="store_true", help="Simulate immediate WhatsApp approval")
    parser.add_argument("--dry-run", action="store_true", help="Run without posting to Instagram")

    args = parser.parse_args()

    print("🚀 ========================================================")
    print("🇯🇵 神谷塾 (@japones_kamiyajuku) Instagram Multi-Agent System")
    print("🚀 ========================================================")

    supervisor = SupervisorAgent()

    # Step 1: パイプライン実行（企画 → コピー作成 → カルーセル/ストーリー準備 → Supervisor QA → WhatsAppプレビュー）
    print("\n[1/3] 🤖 Running multi-agent content creation pipeline...")
    package = supervisor.run_creation_pipeline(specific_theme=args.theme, is_story=args.story)

    print(f"✅ Package Created: {package.post_id}")
    print(f"📂 Category: {package.metadata.category.value}")
    print(f"🎯 Target Level: {package.metadata.target_level.value}")
    print(f"🏷️ CTA Trigger: {package.content.cta_trigger_word}")
    print(f"🖼️ Slides Generated: {len(package.visuals.slides)} items")
    for s in package.visuals.slides:
        print(f"   Slide #{s.slide_index}: {s.image_path}")

    print("\n📝 [Preview Caption]:")
    print(package.content.caption_full)

    # Step 2: 承認シミュレーション
    if args.simulate_approval:
        print("\n[2/3] 📱 Simulating WhatsApp Admin Reply: '承認'...")
        result = supervisor.handle_admin_decision(package, reply_text="承認")
        print(f"🎉 Result: {result}")
    else:
        print("\n[2/3] ⏳ Status: PENDING_HUMAN_APPROVAL. Waiting for WhatsApp response via Webhook.")

    print("\n[3/3] 📜 Pipeline Audit Logs:")
    for log in package.audit_logs:
        print(f"   {log}")

if __name__ == "__main__":
    main()
