import os
import json
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error
    import urllib.parse
from typing import List, Dict, Any, Optional
from config import settings

class InstagramAPIClient:
    """
    Instagram Graph API Client for Carousel / Single Post Publishing
    """
    def __init__(self, account_id: Optional[str] = None, access_token: Optional[str] = None):
        self.account_id = account_id or settings.INSTAGRAM_ACCOUNT_ID
        self.access_token = access_token or settings.INSTAGRAM_ACCESS_TOKEN
        self.app_id = getattr(settings, "META_APP_ID", "1371926405077429")
        self.app_secret = getattr(settings, "META_APP_SECRET", "")
        self.base_url = "https://graph.facebook.com/v20.0"

    def is_configured(self) -> bool:
        return bool(self.account_id and self.access_token and "xxx" not in self.access_token)

    def check_and_auto_refresh_token(self) -> Dict[str, Any]:
        """
        アクセストークンの有効期限を自動確認し、必要に応じて自動更新（リフレッシュ）する。
        """
        if not self.is_configured():
            return {"status": "UNCONFIGURED"}

        from datetime import datetime
        debug_url = f"{self.base_url}/debug_token"
        try:
            res = requests.get(debug_url, params={
                "input_token": self.access_token,
                "access_token": self.access_token
            }, timeout=10)
            data = res.json().get("data", {})
            expires_at = data.get("expires_at", 0)
            is_valid = data.get("is_valid", False)

            if not is_valid:
                print("⚠️ アクセストークンが無効です。")
                return {"status": "INVALID", "message": "Token is invalid"}

            days_left = 999
            if expires_at:
                exp_date = datetime.fromtimestamp(expires_at)
                days_left = (exp_date - datetime.now()).days
                print(f"ℹ️ トークン有効期限: {exp_date} (残り {days_left} 日)")

            # 有効期限が30日未満、または短期トークン（0〜5日）の場合に自動延長を試行
            if days_left < 30 and self.app_secret:
                print(f"🔄 トークンの自動延長（リフレッシュ）を実行中...")
                refresh_res = requests.get(f"{self.base_url}/oauth/access_token", params={
                    "grant_type": "fb_exchange_token",
                    "client_id": self.app_id,
                    "client_secret": self.app_secret,
                    "fb_exchange_token": self.access_token
                }, timeout=10).json()

                if "access_token" in refresh_res:
                    new_token = refresh_res["access_token"]
                    self.access_token = new_token
                    # .env ファイルを更新
                    self._update_env_token(new_token)
                    print(f"✅ トークンの自動延長に成功しました！(新しい有効期限: +60日)")
                    return {"status": "REFRESHED", "new_token": new_token, "days_left": 60}
                else:
                    print(f"⚠️ トークン自動延長APIエラー: {refresh_res}")

            return {"status": "VALID", "days_left": days_left}
        except Exception as e:
            print(f"⚠️ トークン期限チェック中にエラー: {e}")
            return {"status": "ERROR", "error": str(e)}

    def _update_env_token(self, new_token: str):
        """ .env ファイル内の INSTAGRAM_ACCESS_TOKEN を安全に書き換え """
        env_path = settings.BASE_DIR / ".env"
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
            import re
            new_content = re.sub(
                r'INSTAGRAM_ACCESS_TOKEN="[^"]*"',
                f'INSTAGRAM_ACCESS_TOKEN="{new_token}"',
                content
            )
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(new_content)

    def create_carousel_item(self, image_url: str) -> str:
        """カルーセルの個別アイテムコンテナ作成"""
        url = f"{self.base_url}/{self.account_id}/media"
        params = {
            "image_url": image_url,
            "is_carousel_item": "true",
            "access_token": self.access_token
        }
        res = requests.post(url, params=params)
        res.raise_for_status()
        return res.json()["id"]

    def create_carousel_container(self, item_ids: List[str], caption: str) -> str:
        """カルーセル親コンテナ作成"""
        url = f"{self.base_url}/{self.account_id}/media"
        params = {
            "media_type": "CAROUSEL",
            "children": ",".join(item_ids),
            "caption": caption,
            "access_token": self.access_token
        }
        res = requests.post(url, params=params)
        res.raise_for_status()
        return res.json()["id"]

    def publish_media(self, creation_id: str) -> Dict[str, Any]:
        """作成したコンテナを公開実行"""
        url = f"{self.base_url}/{self.account_id}/media_publish"
        params = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        res = requests.post(url, params=params)
        res.raise_for_status()
        return res.json()

    def publish_story(self, image_url: str) -> Dict[str, Any]:
        """Instagram ストーリーズへの単発投稿 (media_type: STORIES)"""
        if not self.is_configured():
            return {
                "status": "SIMULATED",
                "media_type": "STORIES",
                "message": "Instagram API credentials not set. Simulating successful Story publish.",
                "post_id": "simulated_ig_story_12345"
            }

        url = f"{self.base_url}/{self.account_id}/media"
        params = {
            "image_url": image_url,
            "media_type": "STORIES",
            "access_token": self.access_token
        }
        res = requests.post(url, params=params) if HAS_REQUESTS else self._urllib_post(url, params)
        res.raise_for_status() if HAS_REQUESTS else None
        container_id = res.json()["id"] if HAS_REQUESTS else res["id"]

        publish_result = self.publish_media(container_id)
        return publish_result

    def upload_local_image(self, file_path: str) -> str:
        """ローカルの画像をInstagramが取得できる一時パブリックURLへアップロード"""
        if file_path.startswith("http://") or file_path.startswith("https://"):
            return file_path
        
        try:
            with open(file_path, "rb") as f:
                res = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f})
                res.raise_for_status()
                return res.text.strip()
        except Exception as e:
            print(f"Error uploading image {file_path}: {e}")
            raise

    def publish_carousel_post(self, public_image_urls: List[str], caption: str) -> Dict[str, Any]:
        """カルーセル（フィード投稿）の一括公開パイプライン"""
        if not self.is_configured():
            return {
                "status": "SIMULATED",
                "media_type": "CAROUSEL",
                "message": "Instagram API credentials not set. Simulating successful Carousel publish.",
                "post_id": "simulated_ig_post_12345"
            }

        # 投稿前にトークンの有効期限を確認＆自動更新
        self.check_and_auto_refresh_token()

        # ローカルパスが含まれる場合は自動アップロード
        uploaded_urls = []
        for img in public_image_urls:
            uploaded_urls.append(self.upload_local_image(img))

        item_ids = [self.create_carousel_item(url) for url in uploaded_urls]
        container_id = self.create_carousel_container(item_ids, caption)
        publish_result = self.publish_media(container_id)
        return publish_result
