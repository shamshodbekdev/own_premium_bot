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

from app.database.db import async_session
from app.database.crud import get_pending_payment, update_payment_status, update_balance
from app.database.models import TransactionType

@router.callback_query(F.data.startswith("admin_approve_"))
async def approve_payment(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        return
    
    payment_id = int(callback.data.split("_")[-1])
    
    async with async_session() as session:
        payment = await get_pending_payment(session, payment_id)
        if not payment or payment.status != "pending":
            await callback.answer("Bu to'lov allaqachon ko'rib chiqilgan!", show_alert=True)
            return
        
        await update_payment_status(session, payment_id, "approved")
        await update_balance(
            session, 
            payment.user_id, 
            payment.amount, 
            TransactionType.DEPOSIT, 
            "Hisobni to'ldirish"
        )
    
    await callback.message.edit_caption(
        caption=f"✅ To'lov tasdiqlandi!\nFoydalanuvchi ID: {payment.user_id}\nSumma: {payment.amount:,.0f} so'm"
    )
    
    # Foydalanuvchiga xabar yuborish
    try:
        await bot.send_message(
            payment.user_id,
            f"✅ To'lovingiz tasdiqlandi!\nBalansingizga {payment.amount:,.0f} so'm qo'shildi."
        )
    except Exception:
        pass
    
    await callback.answer("Tasdiqlandi!")

@router.callback_query(F.data.startswith("admin_reject_"))
async def reject_payment(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    payment_id = int(callback.data.split("_")[-1])
    
    async with async_session() as session:
        payment = await get_pending_payment(session, payment_id)
        if payment:
            await update_payment_status(session, payment_id, "rejected")
    
    await callback.message.edit_caption(
        caption=f"❌ To'lov rad etildi.\nFoydalanuvchi ID: {payment.user_id}"
    )
    await callback.answer("Rad etildi!")