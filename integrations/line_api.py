import os
import requests
from typing import List, Dict, Any, Optional
from config import settings

class LineNotificationClient:
    """
    LINE Messaging API 連携クライアント
    投稿前の画像プレビュー・キャプション・承認ボタンをスマホのLINEへ送信
    """
    def __init__(self, channel_access_token: Optional[str] = None):
        self.access_token = channel_access_token or getattr(settings, "LINE_CHANNEL_ACCESS_TOKEN", "")
        self.user_id = getattr(settings, "LINE_USER_ID", "")
        self.base_url = "https://api.line.me/v2/bot/message"

    def is_configured(self) -> bool:
        return bool(self.access_token and "xxx" not in self.access_token)

    def send_preview_for_approval(self, title: str, slide_image_urls: List[str], caption: str, post_id: str) -> Dict[str, Any]:
        """LINEへ画像プレビューと承認ボタンを送信"""
        if not self.is_configured():
            print("⚠️ LINE APIトークンが未設定です。.env に LINE_CHANNEL_ACCESS_TOKEN を設定してください。")
            return {"status": "NOT_CONFIGURED"}

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # 1. プレビューメッセージの構築（Flex Message または テキスト＋画像）
        cover_img = slide_image_urls[0] if slide_image_urls else "https://via.placeholder.com/1080x1350"
        
        # Flex Message (見栄えの良いリッチカード)
        flex_message = {
            "type": "flex",
            "altText": f"⛩️【神谷塾】新しい投稿の確認依頼: {title}",
            "contents": {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": cover_img,
                    "size": "full",
                    "aspectRatio": "4:5",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "⛩️ 神谷塾 投稿承認リクエスト",
                            "weight": "bold",
                            "color": "#2A5A35",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": title,
                            "weight": "bold",
                            "size": "lg",
                            "margin": "md",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": f"スライド画像: 全{len(slide_image_urls)}枚\nキャプション:\n{caption[:120]}...",
                            "size": "xs",
                            "color": "#666666",
                            "margin": "md",
                            "wrap": True
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "color": "#E8822A",
                            "action": {
                                "type": "message",
                                "label": "✅ 承認してInstagramに投稿",
                                "text": f"APPROVE_{post_id}"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "🔄 今回は見送る / 修正",
                                "text": f"REJECT_{post_id}"
                            }
                        }
                    ]
                }
            }
        }

        payload = {
            "to": self.user_id,
            "messages": [flex_message]
        }

        url = f"{self.base_url}/push"
        try:
            res = requests.post(url, headers=headers, json=payload)
            res.raise_for_status()
            print(f"✅ スマホのLINEへ承認プレビューを送信しました！ (To: {self.user_id})")
            return res.json()
        except Exception as e:
            print(f"❌ LINE送信エラー: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"   詳細: {e.response.text}")
            return {"error": str(e)}

    def send_simple_text(self, text: str) -> Dict[str, Any]:
        """シンプルなテキスト通知"""
        if not self.is_configured():
            return {"status": "NOT_CONFIGURED"}
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": self.user_id,
            "messages": [{"type": "text", "text": text}]
        }
        res = requests.post(f"{self.base_url}/push", headers=headers, json=payload)
        return res.json()
