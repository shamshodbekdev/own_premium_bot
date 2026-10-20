from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from config import Config
from app.keyboards.inline import InlineKeyboards

router = Router()

# Admin huquqini tekshirish (Faqat ADMIN_ID ga ruxsat)
def is_admin(user_id: int) -> bool:
    return user_id == Config.ADMIN_ID

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(
        "⚙️ <b>Admin Panel</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=InlineKeyboards.admin_menu()
    )

@router.callback_query(F.data == "admin_panel")
async def admin_panel_cb(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Sizda ruxsat yo'q!", show_alert=True)
        return
    await callback.message.edit_text(
        "⚙️ <b>Admin Panel</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=InlineKeyboards.admin_menu()
    )
    await callback.answer()

@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    # Hozircha statik, keyin bazadan olamiz
    text = (
        "📊 <b>Statistika</b>\n\n"
        "👥 Foydalanuvchilar: 0\n"
        "💰 Umumiy tushum: 0 so'm\n"
        "📦 Sotilgan Premium: 0 ta"
    )
    await callback.message.edit_text(text, reply_markup=InlineKeyboards.back_to_main())
    await callback.answer()

@router.callback_query(F.data == "admin_pending_payments")
async def pending_payments(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    await callback.message.edit_text(
        "💳 <b>Kutilayotgan To'lovlar</b>\n\nHozircha to'lovlar yo'q.",
        reply_markup=InlineKeyboards.back_to_main()
    )
    await callback.answer()