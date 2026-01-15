---
name: Скелет Telegram бота на aiogram
overview: Создание базовой структуры Telegram бота на aiogram 3.24.0 с основными файлами конфигурации, обработчиками команд /start и /help, и необходимой документацией.
todos: []
---

# Создание базового скелета Telegram бота на aiogram

## Структура проекта

Создадим следующую структуру файлов:

```
c:\projects\1_appka\
├── .env                    # Переменные окружения (не в git)
├── .env.example            # Пример конфигурации
├── .gitignore              # Уже существует
├── bot.py                  # Основной файл бота
├── requirements.txt        # Зависимости Python
├── README.md               # Документация
└── public/                 # Уже существует (Web App)
    └── index.html
```

## Детальный план

### 1. Основной файл бота (`bot.py`)

Создадим главный файл с:

- Инициализацией Bot и Dispatcher согласно документации aiogram 3.24.0
- Обработчиком команды `/start` с использованием `CommandStart()` фильтра
- Обработчиком команды `/help` 
- Базовым echo-обработчиком для демонстрации
- Настройкой логирования
- Функцией `main()` для запуска через `asyncio.run()`
- Использованием `DefaultBotProperties` с HTML parse mode

Структура кода:

```python
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

# Конфигурация
TOKEN = getenv("BOT_TOKEN")

# Dispatcher
dp = Dispatcher()

# Обработчики команд
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    ...

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    ...

@dp.message()
async def echo_handler(message: Message) -> None:
    ...

# Функция запуска
async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
```

### 2. Файл зависимостей (`requirements.txt`)

Добавим необходимые пакеты:

- `aiogram>=3.24.0` - основная библиотека
- `python-dotenv>=1.0.0` - для работы с .env файлами

### 3. Конфигурация (`.env.example`)

Создадим пример файла с переменными:

- `BOT_TOKEN=` - токен бота от @BotFather

### 4. Обновление `.gitignore`

Убедимся, что `.env` файл игнорируется (уже есть в списке).

### 5. Документация (`README.md`)

Создадим README с:

- Описанием проекта
- Инструкциями по установке
- Примером настройки .env файла
- Командами для запуска
- Ссылками на документацию aiogram

## Особенности реализации

1. **Следование документации aiogram 3.24.0**:

   - Использование `DefaultBotProperties` для настроек по умолчанию
   - Правильная инициализация через `Dispatcher()`
   - Использование новых фильтров `CommandStart()` и `Command()`

2. **Безопасность**:

   - Токен бота хранится в переменных окружения
   - `.env` файл не коммитится в git

3. **Расширяемость**:

   - Структура позволяет легко добавлять новые обработчики
   - Код следует best practices из документации

4. **Простота**:

   - Все в одном файле для начала
   - Минимальные зависимости
   - Понятная структура кода

## Следующие шаги (опционально)

После создания базового скелета можно будет расширить:

- Добавить Router для модульной структуры
- Реализовать middleware для логирования
- Добавить обработку ошибок
- Создать примеры клавиатур
- Интегрировать FSM для диалогов