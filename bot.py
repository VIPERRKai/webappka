import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from middleware import AuthMiddleware, ThrottlingMiddleware, is_admin
from admin import show_admin_menu, handle_admin_panel_callback

# Load environment variables from .env file
load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Регистрируем middleware
# ThrottlingMiddleware должен быть первым, чтобы ограничивать все запросы
dp.message.middleware(ThrottlingMiddleware(rate_limit=1.0))
dp.callback_query.middleware(ThrottlingMiddleware(rate_limit=1.0))
dp.message.middleware(AuthMiddleware())


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    Проверяет, является ли пользователь админом, и показывает админ меню если да.
    """
    if not message.from_user:
        return
    
    # Проверяем, является ли пользователь админом
    if is_admin(message.from_user.id):
        # Показываем админ меню
        await show_admin_menu(message)
    else:
        await message.answer(
            f"Hello, {html.bold(message.from_user.full_name)}!\n\n"
            f"Это базовый скелет Telegram бота на aiogram 3.24.0.\n"
            f"Используйте /help для просмотра доступных команд."
        )


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    help_text = (
        f"{html.bold('Доступные команды:')}\n\n"
        f"/start - Начать работу с ботом\n"
        f"/help - Показать эту справку\n\n"
        f"Вы можете отправлять любые сообщения боту, и он будет их повторять."
    )
    await message.answer(help_text)


@dp.callback_query(lambda c: c.data == "admin_panel")
async def admin_panel_callback_handler(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку "Админ панель"
    """
    await handle_admin_panel_callback(callback)


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        # Run events dispatching with polling
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
