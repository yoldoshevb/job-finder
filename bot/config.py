import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot konfiguratsiyasi"""
    
    # Bot token
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Adminlar (vergul bilan ajratilgan ID'lar)
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    
    # AI model
    AI_MODEL = "all-MiniLM-L6-v2"  # HuggingFace modeli
    
    # Match score threshold
    MATCH_THRESHOLD = 60  # 60% dan yuqori bo'lsa ko'rsatish
    
    # Max photos per job
    MAX_PHOTOS = 3
    
    # Max file size (MB)
    MAX_FILE_SIZE = 20
    
    @classmethod
    def validate(cls):
        """Konfiguratsiyani tekshirish"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL topilmadi! .env faylini tekshiring.")
        print("✅ Konfiguratsiya tayyor!")
