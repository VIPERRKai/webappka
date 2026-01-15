from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import html
from middleware import is_admin


def get_admin_menu() -> InlineKeyboardMarkup:
    """
    Создает админ меню с кнопками.
    
    Returns:
        InlineKeyboardMarkup с кнопками админ меню
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Админ панель", callback_data="admin_panel")
            ]
        ]
    )
    return keyboard


async def show_admin_menu(message: Message) -> None:
    """
    Показывает админ меню пользователю.
    
    Args:
        message: Сообщение от пользователя
    """
    if not message.from_user:
        return
    
    # Проверяем, является ли пользователь админом
    if is_admin(message.from_user.id):
        await message.answer(
            f"👋 Добро пожаловать, {html.bold(message.from_user.full_name)}!\n\n"
            f"🔐 Вы авторизованы как администратор.\n"
            f"Выберите действие:",
            reply_markup=get_admin_menu()
        )
    else:
        await message.answer(
            "❌ Доступ запрещен. Этот бот доступен только администратору."
        )


async def handle_admin_panel_callback(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку "Админ панель".
    
    Args:
        callback: Callback запрос от кнопки
    """
    if not callback.from_user:
        return
    
    # Проверяем, является ли пользователь админом
    if is_admin(callback.from_user.id):
        await callback.answer("Вы админ")
        await callback.message.answer("Я админ")
    else:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
