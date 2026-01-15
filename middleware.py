import time
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable, Union

# Admin user ID
ADMIN_ID = 1174881844


class AuthMiddleware(BaseMiddleware):
    """
    Middleware для проверки авторизации пользователя.
    Разрешает доступ только администратору с указанным ID.
    """
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Проверяем ID пользователя
        user_id = event.from_user.id if event.from_user else None
        
        if user_id != ADMIN_ID:
            # Если пользователь не админ, отправляем сообщение и блокируем обработку
            await event.answer(
                f"❌ Доступ запрещен. Этот бот доступен только администратору."
            )
            return
        
        # Если пользователь админ, продолжаем обработку
        return await handler(event, data)


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware для ограничения частоты запросов от пользователей.
    Ограничивает количество действий до 1 раза в 0.5 секунды.
    """
    
    def __init__(self, rate_limit: float = 0.5):
        """
        Инициализирует ThrottlingMiddleware.
        
        Args:
            rate_limit: Минимальный интервал между запросами в секундах (по умолчанию 0.5)
        """
        self.rate_limit = rate_limit
        self.last_action_time: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        # Получаем ID пользователя
        user_id = None
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id
        
        if user_id is None:
            # Если не удалось определить пользователя, пропускаем обработку
            return await handler(event, data)
        
        # Получаем текущее время
        current_time = time.time()
        
        # Проверяем, когда был последний запрос от этого пользователя
        if user_id in self.last_action_time:
            time_since_last_action = current_time - self.last_action_time[user_id]
            
            if time_since_last_action < self.rate_limit:
                # Если прошло меньше времени, чем разрешено, блокируем запрос
                remaining_time = self.rate_limit - time_since_last_action
                if isinstance(event, Message):
                    await event.answer(
                        f"⏳ Пожалуйста, подождите {remaining_time:.1f} секунд перед следующим действием."
                    )
                elif isinstance(event, CallbackQuery):
                    await event.answer(
                        f"⏳ Подождите {remaining_time:.1f} сек.",
                        show_alert=False
                    )
                return
        
        # Обновляем время последнего действия
        self.last_action_time[user_id] = current_time
        
        # Продолжаем обработку
        return await handler(event, data)


def is_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором.
    
    Args:
        user_id: ID пользователя для проверки
        
    Returns:
        True если пользователь админ, False в противном случае
    """
    return user_id == ADMIN_ID
