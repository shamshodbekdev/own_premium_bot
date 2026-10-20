import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, FloodWaitError
from config import Config

logger = logging.getLogger(__name__)

class UserbotService:
    def __init__(self):
        self.client = None
        self.phone_code_hash = None
        self.phone = None

    async def send_code(self, phone: str):
        self.phone = phone
        self.client = TelegramClient(StringSession(), Config.API_ID, Config.API_HASH)
        await self.client.connect()
        try:
            sent_code = await self.client.send_code_request(phone)
            self.phone_code_hash = sent_code.phone_code_hash
            return True, "Kod yuborildi"
        except FloodWaitError as e:
            return False, f"Iltimos, {e.seconds} soniya kutib turing."
        except Exception as e:
            return False, str(e)

    async def sign_in(self, code: str = None, password: str = None):
        try:
            if password:
                await self.client.sign_in(password=password)
            else:
                await self.client.sign_in(self.phone, code, phone_code_hash=self.phone_code_hash)
            return True, self.client.session.save()
        except SessionPasswordNeededError:
            return False, "2FA_PASSWORD"
        except PhoneCodeInvalidError:
            return False, "Kod xato"
        except FloodWaitError as e:
            return False, f"Iltimos, {e.seconds} soniya kutib turing."
        except Exception as e:
            return False, str(e)

    def get_payment_url(self) -> str:
        """To'g'ridan-to'g'ri @PremiumBot to'lov havolasini qaytarish."""
        # Bu havola foydalanuvchini @PremiumBot ning to'lov sahifasiga olib boradi
        return "https://t.me/premiumbot?start=pay"