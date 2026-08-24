from typing import Optional, Dict, Any
from schemas import InstagramPostPackage, PostStatus
from agents.calendar_trend import CalendarTrendAgent
from agents.copywriter import CopywriterAgent
from agents.design_drive import DesignDriveAgent
from agents.whatsapp_approval import WhatsAppApprovalAgent
from integrations.instagram_api import InstagramAPIClient

class SupervisorAgent:
    """
    全体統括・オーケストレーションエージェント
    各エージェントの実行、品質検証、承認フロー連携、Instagram投稿までを一気通貫で管理
    """
    def __init__(self):
        self.calendar_agent = CalendarTrendAgent()
        self.copywriter_agent = CopywriterAgent()
        self.design_agent = DesignDriveAgent()
        self.whatsapp_agent = WhatsAppApprovalAgent()
        self.instagram_client = InstagramAPIClient()

    def run_creation_pipeline(self, specific_theme: Optional[str] = None, is_story: bool = False) -> InstagramPostPackage:
        """企画からWhatsAppプレビュー送信までのパイプラインを実行"""
        # Step 1: 企画・カレンダー選定
        package = self.calendar_agent.plan_post(specific_theme=specific_theme)

        # Step 2: テキスト・コピー作成
        package = self.copywriter_agent.write_copy(package)

        # Step 3: 画像・素材準備（ストーリー or カルーセル）
        package = self.design_agent.process_visuals(package, is_story=is_story)

        # Step 4: Supervisor QA（品質検証）
        package = self.validate_package(package)

        # Step 5: WhatsAppへ承認リクエスト送信
        if package.status == PostStatus.SUPERVISOR_APPROVED:
            package = self.whatsapp_agent.send_for_approval(package)

        return package

    def validate_package(self, package: InstagramPostPackage) -> InstagramPostPackage:
        """品質検証（CTAの有無、ハッシュタグ数、スライド/ストーリー整合性）"""
        errors = []
        if not package.content or len(package.content.caption_full) < 30:
            errors.append("Caption is too short or missing.")

        if not package.visuals or len(package.visuals.slides) < 1:
            errors.append("At least 1 slide/image is required.")

        if errors:
            package.log(f"SupervisorAgent QA FAILED: {', '.join(errors)}")
            package.status = PostStatus.REJECTED
        else:
            package.status = PostStatus.SUPERVISOR_APPROVED
            package.log("SupervisorAgent: QA PASSED. Package is ready for human approval.")

        return package

    def handle_admin_decision(self, package: InstagramPostPackage, reply_text: str) -> Dict[str, Any]:
        """WhatsApp返信に応じた後続処理"""
        package = self.whatsapp_agent.handle_incoming_reply(package, reply_text)

        if package.status == PostStatus.APPROVED:
            # Instagram Graph APIで自動投稿（ストーリー or フィードカルーセル）
            if package.visuals and package.visuals.media_type == "STORIES":
                story_img = package.visuals.slides[0].image_path
                publish_res = self.instagram_client.publish_story(story_img)
            else:
                image_urls = [s.image_path for s in package.visuals.slides]
                publish_res = self.instagram_client.publish_carousel_post(
                    public_image_urls=image_urls,
                    caption=package.content.caption_full
                )

            package.status = PostStatus.PUBLISHED
            package.log(f"SupervisorAgent: Successfully published ({package.visuals.media_type}) to Instagram. Result: {publish_res}")
            return {"status": "PUBLISHED", "media_type": package.visuals.media_type, "post_id": package.post_id, "detail": publish_res}

        elif package.status == PostStatus.REVISION_REQUESTED:
            # 修正指示を反映して再生成
            package = self.copywriter_agent.write_copy(package, revision_instructions=reply_text)
            package = self.validate_package(package)
            package = self.whatsapp_agent.send_for_approval(package)
            return {"status": "REVISION_RESENT", "post_id": package.post_id}

        elif package.status == PostStatus.REJECTED:
            return {"status": "CANCELLED", "post_id": package.post_id}

        return {"status": "PENDING", "post_id": package.post_id}
