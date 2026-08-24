import uvicorn
from fastapi import FastAPI, Request, Response, Query, HTTPException
from fastapi.responses import PlainTextResponse
from config import settings
from agents.supervisor import SupervisorAgent

app = FastAPI(title="Kamiyajuku WhatsApp Webhook Service")
supervisor = SupervisorAgent()

# メモリ上のセッションキャッシュ（ID毎のドラフト保持）
post_cache = {}

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    """Meta WhatsApp Webhookの初回接続検証 (Verification Request)"""
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@app.post("/webhook")
async def receive_whatsapp_message(request: Request):
    """WhatsAppからの返答（承認・修正指示）を受信してSupervisor Agentへ伝達"""
    data = await request.json()

    # Meta Webhookのペイロード解析
    try:
        entries = data.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    sender_phone = msg.get("from")
                    msg_text = msg.get("text", {}).get("body", "")

                    if msg_text:
                        print(f"📩 Received WhatsApp Message from {sender_phone}: {msg_text}")
                        # 直近の最新ドラフトパッケージに対して判定
                        if post_cache:
                            latest_post_id = list(post_cache.keys())[-1]
                            package = post_cache[latest_post_id]
                            result = supervisor.handle_admin_decision(package, msg_text)
                            print(f"⚡ Handled decision for {latest_post_id}: {result}")

        return {"status": "SUCCESS"}
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return {"status": "ERROR", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.WEBHOOK_HOST, port=settings.WEBHOOK_PORT)
