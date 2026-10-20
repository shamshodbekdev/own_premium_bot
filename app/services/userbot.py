import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, FloodWaitError, ResendCodeRequest
from config import Config

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
        except ResendCodeRequest:
            return False, "Iltimos, 1-2 daqiqa kutib, qayta urinib ko'ring."
        except Exception as e:
            return False, str(e)

    async def purchase_premium(self, session_string: str):
        """@PremiumBot orqali 1 oylik Premium sotib olish va 3DS havolasini olish."""
        client = TelegramClient(StringSession(session_string), Config.API_ID, Config.API_HASH)
        await client.connect()
        
        try:
            # @PremiumBot ga /start yuborish
            await client.send_message('@PremiumBot', '/start')
            await asyncio.sleep(3)
            
            # Oxirgi xabarlarni olish
            messages = await client.get_messages('@PremiumBot', limit=3)
            invoice_btn = None
            
            # "Pay 35 990,00 UZS" tugmasini qidirish
            for msg in messages:
                if msg.buttons:
                    for row in msg.buttons:
                        for btn in row:
                            if "pay" in btn.text.lower() and "uzs" in btn.text.lower():
                                invoice_btn = btn
                                break
                    if invoice_btn:
                        break
            
            if not invoice_btn:
                return False, "To'lov tugmasi topilmadi. @PremiumBot interfeysi o'zgargan bo'lishi mumkin."
            
            # To'lov tugmasini bosish
            await invoice_btn.click()
            await asyncio.sleep(3)
            
            # Karta ma'lumotlarini kiritish (rasmlaringizdagi ketma-ketlik)
            # 1. Karta raqami
            await client.send_message('@PremiumBot', Config.ADMIN_CARD_NUMBER)
            await asyncio.sleep(2)
            
            # 2. Amal qilish muddati (MM/YY)
            await client.send_message('@PremiumBot', Config.ADMIN_CARD_EXPIRY)
            await asyncio.sleep(2)
            
            # 3. CVV kod
            await client.send_message('@PremiumBot', Config.ADMIN_CARD_CVV)
            await asyncio.sleep(5)  # 3DS so'rovi kelishini kutish
            
            # 3DS havolasini qidirish (api.checkout.com yoki shunga o'xshash)
            messages = await client.get_messages('@PremiumBot', limit=5)
            for msg in messages:
                if msg.text and ("http" in msg.text or "3ds" in msg.text.lower()):
                    # 3DS havolasini topdik
                    return True, msg.text
            
            return False, "3DS havolasi topilmadi. Iltimos, qo'lda tekshiring."
        except Exception as e:
            return False, f"Xatolik: {str(e)}"
        finally:
            await client.disconnect()

    async def cleanup_and_logout(self, session_string: str):
        """Yozishmalarni tozalash va akkauntdan chiqish."""
        client = TelegramClient(StringSession(session_string), Config.API_ID, Config.API_HASH)
        await client.connect()
        try:
            await client.delete_dialog('@PremiumBot')
            await client.log_out()
            return True, "Tozalandi"
        except Exception as e:
            return False, str(e)