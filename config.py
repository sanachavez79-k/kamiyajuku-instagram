import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Optional python-dotenv or manual parser
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class Settings:
    # Meta / Instagram
    INSTAGRAM_ACCOUNT_ID: str = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
    INSTAGRAM_ACCESS_TOKEN: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    META_APP_ID: str = os.getenv("META_APP_ID", "1371926405077429")
    META_APP_SECRET: str = os.getenv("META_APP_SECRET", "")
    
    # WhatsApp
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    ADMIN_WHATSAPP_NUMBER: str = os.getenv("ADMIN_WHATSAPP_NUMBER", "")
    WHATSAPP_VERIFY_TOKEN: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "kamiyajuku_secret")
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # AI / Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Drive / Local Paths
    BASE_DIR: Path = BASE_DIR
    GENERATED_ASSETS_DIR: Path = BASE_DIR / "generated_assets"
    DEFAULT_LOCAL_CONTENT_DIR: str = os.getenv(
        "LOCAL_CONTENT_DIR", 
        str(Path(BASE_DIR).parent / "インスタグラム　コンテンツ")
    )
    
    # Server
    WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT", 8000))
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "0.0.0.0")

settings = Settings()
settings.GENERATED_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
