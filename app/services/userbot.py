import asyncio
import logging
import re
from telethon import TelegramClient, types
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

    async def get_payment_url(self, session_string: str):
        """@PremiumBot dan 3DS to'lov havolasini olish."""
        client = TelegramClient(StringSession(session_string), Config.API_ID, Config.API_HASH)
        await client.connect()
        
        try:
            logger.info("=== TO'LOV HAVOLASI OLINMOQDA ===")
            await client.send_message('@PremiumBot', '/start')
            await asyncio.sleep(3)
            
            # 1. "Pay" tugmasini topish va bosish
            messages = await client.get_messages('@PremiumBot', limit=5)
            pay_btn = None
            for msg in messages:
                if msg.buttons:
                    for row in msg.buttons:
                        for btn in row:
                            if "pay" in btn.text.lower() or "to'lash" in btn.text.lower():
                                pay_btn = btn
                                break
                    if pay_btn:
                        break
            
            if not pay_btn:
                return False, "To'lov tugmasi topilmadi."
            
            await pay_btn.click()
            logger.info("To'lov tugmasi bosildi. Karta ma'lumotlari kiritilmoqda...")
            await asyncio.sleep(3)
            
            # 2. Karta ma'lumotlarini yuborish (ketma-ketlik rasmlardagi kabi)
            await client.send_message('@PremiumBot', Config.ADMIN_CARD_NUMBER)
            await asyncio.sleep(2)
            await client.send_message('@PremiumBot', Config.ADMIN_CARD_EXPIRY)
            await asyncio.sleep(2)
            await client.send_message('@PremiumBot', Config.ADMIN_CARD_CVV)
            await asyncio.sleep(5)  # 3DS javobini kutish
            
            # 3. 3DS havolasini qidirish
            messages = await client.get_messages('@PremiumBot', limit=10)
            for msg in messages:
                if msg.text:
                    urls = re.findall(r'https?://[^\s]+', msg.text)
                    if urls:
                        return True, urls[0]
                if msg.entities:
                    for entity in msg.entities:
                        if isinstance(entity, types.MessageEntityTextUrl):
                            return True, entity.url
            
            return False, "3DS havolasi topilmadi. Iltimos, @PremiumBot javobini tekshiring."
        except Exception as e:
            logger.error(f"Xatolik: {e}")
            return False, str(e)
        finally:
            await client.disconnect()