from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

class InlineKeyboards:
    """Botning barcha inline klaviaturalari markazlashtirilgan holda."""

    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        
        builder.button(
            text="⭐️ 1 Oylik Premium Olish", 
            callback_data="buy_premium",
            style="success" # Yashil
        )
        builder.button(
            text="💳 Hisobni To'ldirish", 
            callback_data="top_up",
            style="primary" # Ko'k
        )
        builder.button(
            text="👤 Mening Profilim", 
            callback_data="profile",
            style="primary" # Ko'k
        )
        builder.button(
            text="⚙️ Admin Panel", 
            callback_data="admin_panel",
            style="danger" # Qizil
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def payment_check() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="✅ Tasdiqlash", 
            callback_data="admin_approve_payment",
            style="success" # Yashil
        )
        builder.button(
            text="❌ Rad Etish", 
            callback_data="admin_reject_payment",
            style="danger" # Qizil
        )
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    def userbot_link() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="📱 Akkauntni Ulash", 
            callback_data="link_userbot",
            style="primary" # Ko'k
        )
        builder.button(
            text="🚫 Bekor Qilish", 
            callback_data="cancel_action",
            style="danger" # Qizil
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def admin_menu() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="📊 Statistika", 
            callback_data="admin_stats",
            style="primary"
        )
        builder.button(
            text="💳 Kutilayotgan To'lovlar", 
            callback_data="admin_pending_payments",
            style="success"
        )
        builder.button(
            text="📢 Xabar Yuborish (Broadcast)", 
            callback_data="admin_broadcast",
            style="primary"
        )
        builder.button(
            text="🔙 Orqaga", 
            callback_data="back_to_main",
            style="danger"
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def back_to_main() -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="🔙 Asosiy Menyu", 
            callback_data="back_to_main",
            style="danger"
        )
        return builder.as_markup()