import json
from datetime import datetime
from typing import Dict, Any, Optional
from schemas import InstagramPostPackage, ApprovalState, PostStatus
from integrations.whatsapp_api import WhatsAppAPIClient
from config import settings

class WhatsAppApprovalAgent:
    """
    WhatsApp承認連携エージェント
    完成した投稿パッケージ（画像プレビュー・キャプション要約）を管理者のWhatsAppへ送信し、
    返信（承認 / 修正指示）を処理
    """
    def __init__(self):
        self.client = WhatsAppAPIClient()
        self.admin_phone = settings.ADMIN_WHATSAPP_NUMBER

    def send_for_approval(self, package: InstagramPostPackage) -> InstagramPostPackage:
        if not package.content or not package.visuals:
            raise ValueError("Cannot send approval for incomplete post package.")

        first_slide = package.visuals.slides[0].image_path
        total_slides = len(package.visuals.slides)
        caption_preview = package.content.caption_full[:300]

        message = (
            f"📸 *【神谷塾 Instagram投稿 承認リクエスト】*\n\n"
            f"🆔 ID: `{package.post_id}`\n"
            f"📂 カテゴリ: {package.metadata.category.value}\n"
            f"🎯 目標: {package.metadata.goal} (CTA: {package.content.cta_trigger_word})\n"
            f"🖼 スライド枚数: {total_slides}枚\n\n"
            f"📝 *キャプションプレビュー:*\n"
            f"{caption_preview}...\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"以下のいずれかで返信してください:\n"
            f"✅ *「承認」* または *「1」* → Instagramへ自動投稿\n"
            f"✏️ *「修正: 〇〇」* → 指示に従い再生成\n"
            f"❌ *「破棄」* → キャンセル"
        )

        res = self.client.send_image_preview(
            to_phone=self.admin_phone,
            image_url=first_slide,
            caption=message
        )

        package.approval = ApprovalState(
            whatsapp_message_id=res.get("messages", [{}])[0].get("id", "simulated_msg_id"),
            status=PostStatus.PENDING_HUMAN_APPROVAL
        )
        package.status = PostStatus.PENDING_HUMAN_APPROVAL
        package.log(f"WhatsAppApprovalAgent: Sent preview to admin WhatsApp ({self.admin_phone}).")
        return package

    def handle_incoming_reply(self, package: InstagramPostPackage, reply_text: str) -> InstagramPostPackage:
        cleaned = reply_text.strip().lower()
        now = datetime.now()

        if cleaned in ["承認", "ok", "1", "aprobar", "si", "yes"]:
            package.status = PostStatus.APPROVED
            if package.approval:
                package.approval.status = PostStatus.APPROVED
                package.approval.reviewed_at = now
            package.log("WhatsAppApprovalAgent: Admin approved the post.")
        elif cleaned.startswith("修正") or cleaned.startswith("corregir") or cleaned.startswith("edit"):
            package.status = PostStatus.REVISION_REQUESTED
            if package.approval:
                package.approval.status = PostStatus.REVISION_REQUESTED
                package.approval.review_comments = reply_text
                package.approval.reviewed_at = now
            package.log(f"WhatsAppApprovalAgent: Revision requested: '{reply_text}'.")
        elif cleaned in ["破棄", "cancelar", "9", "rechazar"]:
            package.status = PostStatus.REJECTED
            if package.approval:
                package.approval.status = PostStatus.REJECTED
                package.approval.reviewed_at = now
            package.log("WhatsAppApprovalAgent: Admin rejected the post.")
        else:
            package.log(f"WhatsAppApprovalAgent: Unrecognized admin reply: '{reply_text}'.")

        return package
