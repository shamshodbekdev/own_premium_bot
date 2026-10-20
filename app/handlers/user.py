from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards.inline import InlineKeyboards
from app.database.db import async_session
from app.database.crud import get_or_create_user, get_user_balance
from app.database.models import TransactionType
from config import Config

router = Router()

# FSM Holatlari (Hisobni to'ldirish uchun)
class TopUpStates(StatesGroup):
    waiting_for_receipt = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    async with async_session() as session:
        user = await get_or_create_user(
            session, 
            message.from_user.id, 
            message.from_user.full_name, 
            message.from_user.username
        )
    
    welcome_text = (
        f"Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n\n"
        f"Bu bot orqali siz Telegram Premium obunasini avtomatik sotib olishingiz mumkin.\n\n"
        f"💰 Balansingiz: <b>{user.balance:,.0f} so'm</b>\n\n"
        f"Quyidagi menyudan kerakli bo'limni tanlang:"
    )
    await message.answer(welcome_text, reply_markup=InlineKeyboards.main_menu())

@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    async with async_session() as session:
        balance = await get_user_balance(session, callback.from_user.id)
    
    text = (
        f"👤 <b>Sizning Profilingiz</b>\n\n"
        f"🆔 ID: <code>{callback.from_user.id}</code>\n"
        f"👤 Ism: {callback.from_user.full_name}\n"
        f"💰 Balans: <b>{balance:,.0f} so'm</b>"
    )
    await callback.message.edit_text(text, reply_markup=InlineKeyboards.back_to_main())
    await callback.answer()

@router.callback_query(F.data == "top_up")
async def top_up_start(callback: CallbackQuery, state: FSMContext):
    text = (
        f"💳 <b>Hisobni To'ldirish</b>\n\n"
        f"Quyidagi kartaga <b>{Config.PREMIUM_PRICE:,.0f} so'm</b> yoki o'zingiz xohlagan summani o'tkazing:\n\n"
        f"💳 Karta raqami: <code>{Config.ADMIN_CARD_NUMBER}</code>\n"
        f"👤 Karta egasi: {Config.ADMIN_CARD_HOLDER}\n\n"
        f"To'lovni amalga oshirgandan so'ng, <b>chekni (skrinshotni)</b> shu yerga yuboring."
    )
    await callback.message.edit_text(text, reply_markup=InlineKeyboards.back_to_main())
    await state.set_state(TopUpStates.waiting_for_receipt)
    await callback.answer()

@router.message(TopUpStates.waiting_for_receipt, F.photo)
async def process_receipt(message: Message, state: FSMContext):
    # Admin tasdiqlashi uchun bazaga yozamiz (keyingi bosqichda to'liq qilamiz)
    photo_id = message.photo[-1].file_id
    
    await message.answer(
        "✅ Chekingiz qabul qilindi. Admin tasdiqlagandan so'ng balansingizga mablag' qo'shiladi.",
        reply_markup=InlineKeyboards.back_to_main()
    )
    
    # Adminga xabar yuborish logikasi (keyingi bosqichda admin.py da)
    await state.clear()

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Asosiy menyu. Kerakli bo'limni tanlang:",
        reply_markup=InlineKeyboards.main_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "guide")
async def show_guide(callback: CallbackQuery):
    text = (
        "📓 <b>Qo'llanma</b>\n\n"
        "1. Avval <b>Pul kiritish</b> bo'limi orqali hisobingizni to'ldiring.\n"
        "2. So'ngra <b>1 Oylik Premium Olish</b> tugmasini bosing.\n"
        "3. Akkauntingizni ulash uchun telefon raqamingizni kiriting.\n"
        "4. Telegram'dan kelgan kodni kiriting.\n"
        "5. Tizim avtomatik ravishda Premium obunani sotib oladi.\n\n"
        "Savollaringiz bo'lsa, adminga murojaat qiling."
    )
    await callback.message.edit_text(text, reply_markup=InlineKeyboards.back_to_main())
    await callback.answer()