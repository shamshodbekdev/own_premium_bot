import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

class Config:
    # Asosiy sozlamalar
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH")
    
    # To'lov sozlamalari
    ADMIN_CARD_NUMBER = os.getenv("ADMIN_CARD_NUMBER")
    ADMIN_CARD_HOLDER = os.getenv("ADMIN_CARD_HOLDER")
    PREMIUM_PRICE = int(os.getenv("PREMIUM_PRICE", 40000))

    # Premium Emoji IDlari (Sizning emojilaringiz bilan almashtiring)
    # Bu IDlarni @EmojiIDbot orqali topishingiz mumkin
    EMOJI = {
        "premium": "5368324170671202286", # Premium yulduz
        "card": "5305763340972843676",    # Karta
        "success": "5303473297071088419", # Tasdiq belgisi
        "error": "5303473297071088419",   # Xato belgisi
        "user": "5305763340972843676",    # Foydalanuvchi
    }