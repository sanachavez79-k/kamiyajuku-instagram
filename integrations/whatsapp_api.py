import os
import json
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error
from typing import Dict, Any, Optional
from config import settings

class WhatsAppAPIClient:
    """
    WhatsApp Cloud API Client (Meta Graph API)
    """
    def __init__(self, phone_number_id: Optional[str] = None, access_token: Optional[str] = None):
        self.phone_number_id = phone_number_id or settings.WHATSAPP_PHONE_NUMBER_ID
        self.access_token = access_token or settings.WHATSAPP_ACCESS_TOKEN
        self.base_url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}"

    def is_configured(self) -> bool:
        return bool(self.phone_number_id and self.access_token and "xxx" not in self.access_token)

    def send_text_message(self, to_phone: str, text: str) -> Dict[str, Any]:
        if not self.is_configured():
            return {
                "status": "SIMULATED",
                "to": to_phone,
                "message_preview": text
            }

        url = f"{self.base_url}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": text}
        }
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def send_image_preview(self, to_phone: str, image_url: str, caption: str) -> Dict[str, Any]:
        if not self.is_configured():
            return {
                "status": "SIMULATED",
                "to": to_phone,
                "image_url": image_url,
                "caption": caption
            }

        url = f"{self.base_url}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "image",
            "image": {
                "link": image_url,
                "caption": caption
            }
        }
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()
