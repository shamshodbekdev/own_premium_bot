from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from config import Config

class UserbotService:
    def __init__(self):
        self.client = None
        self.phone_code_hash = None
        self.phone = None

    async def send_code(self, phone: str):
        """Foydalanuvchi raqamiga Telegram kodini yuborish."""
        self.phone = phone
        self.client = TelegramClient(StringSession(), Config.API_ID, Config.API_HASH)
        await self.client.connect()
        try:
            sent_code = await self.client.send_code_request(phone)
            self.phone_code_hash = sent_code.phone_code_hash
            return True, "Kod yuborildi"
        except Exception as e:
            return False, str(e)

    async def sign_in(self, code: str = None, password: str = None):
        """Kodni yoki parolni tekshirish va sessiya yaratish."""
        try:
            if password:
                # Agar parol kiritilgan bo'lsa, faqat parolni tekshiramiz
                await self.client.sign_in(password=password)
            else:
                # Agar kod kiritilgan bo'lsa, kodni tekshiramiz
                await self.client.sign_in(self.phone, code, phone_code_hash=self.phone_code_hash)
            
            return True, self.client.session.save()
        
        except SessionPasswordNeededError:
            return False, "2FA_PASSWORD"
        except PhoneCodeInvalidError:
            return False, "Kod xato"
        except Exception as e:
            return False, str(e)
        
    async def logout_and_clear(self, session_string: str):
        """Akkauntdan chiqish va yozishmalarni tozalash."""
        client = TelegramClient(StringSession(session_string), Config.API_ID, Config.API_HASH)
        await client.connect()
        try:
            await client.delete_dialog('@PremiumBot')
            await client.log_out()
            return True, "Tozalandi"
        except Exception as e:
            return False, str(e)