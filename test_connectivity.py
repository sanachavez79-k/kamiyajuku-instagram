import os
import requests
from config import settings

def test_whatsapp_connection():
    print("=" * 60)
    print("📱 WhatsApp Cloud API 送信テスト")
    print("=" * 60)

    phone_id = settings.WHATSAPP_PHONE_NUMBER_ID
    token = settings.WHATSAPP_ACCESS_TOKEN
    to_phone = settings.ADMIN_WHATSAPP_NUMBER

    if not phone_id or not token or "xxx" in token:
        print("⚠️ .env ファイルに WhatsApp API の情報がまだ設定されていません。")
        print("   取得した WHATSAPP_PHONE_NUMBER_ID と WHATSAPP_ACCESS_TOKEN を")
        print("   instagram_automation/.env に記入してください。\n")
        return False

    url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # テスト送信メッセージ
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {
            "body": (
                "⛩️ *【神谷塾 Instagram自動化システム】*\n"
                "WhatsApp APIの接続テストに成功しました！🎉\n\n"
                "今後、新しく作成された投稿スライド（全6枚）のプレビューがこのチャットに届きます。"
            )
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res_data = res.json()
        if res.status_code == 200:
            print(f"✅ テストメッセージを送信しました！ ➔ 送信先: +{to_phone}")
            print(f"   Message ID: {res_data.get('messages', [{}])[0].get('id')}")
            return True
        else:
            print(f"❌ 送信エラー (HTTP {res.status_code}): {res_data}")
            return False
    except Exception as e:
        print(f"❌ 接続例外エラー: {e}")
        return False

def test_instagram_connection():
    print("\n" + "=" * 60)
    print("📸 Instagram Graph API 接続確認テスト")
    print("=" * 60)

    ig_id = settings.INSTAGRAM_ACCOUNT_ID
    token = settings.INSTAGRAM_ACCESS_TOKEN

    if not ig_id or not token or "xxx" in token:
        print("⚠️ .env ファイルに Instagram API の情報がまだ設定されていません。")
        return False

    url = f"https://graph.facebook.com/v20.0/{ig_id}"
    params = {
        "fields": "id,username,name,profile_picture_url",
        "access_token": token
    }

    try:
        res = requests.get(url, params=params)
        res_data = res.json()
        if res.status_code == 200:
            print(f"🎉 【大成功】Instagram公式アカウントと完全連携しました！")
            print(f"   👤 アカウント名: @{res_data.get('username')}")
            print(f"   🏷️ プロフィール表示名: {res_data.get('name')}")
            print(f"   🆔 アカウントID: {res_data.get('id')}")
            return True
        else:
            print(f"❌ Instagram認証エラー: {res_data}")
            return False
    except Exception as e:
        print(f"❌ 接続例外エラー: {e}")
        return False

if __name__ == "__main__":
    test_whatsapp_connection()
    test_instagram_connection()
