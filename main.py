from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import asyncio, logging

from linktopngtext.core.handlers.basic import get_url
from linktopngtext.core.handlers.handler import start_command

# Функции для ответов на кнопки
from linktopngtext.core.handlers.callback.screen_file import screen_url
from linktopngtext.core.handlers.callback.text_file import text_url

token = '6113444257:AAEQOIhqKOrmMS02GAxsQB1Cd8dsNzAzfEs'


# Функция запуска бота
async def start():
    bot = Bot(token=token, parse_mode='HTML')  # Создаем объект бота с заданным токеном

    dp = Dispatcher()  # Создаем диспетчер для обработки входящих сообщений и команд

    dp.message.register(start_command, Command(commands=['start']))  # Регистрируем функцию-обработчик команды "/start"
    dp.message.register(get_url)  # Регистрируем функцию-обработчик проверки ссылки

    dp.callback_query.register(screen_url, F.data.startswith('Скрин'))  # Inline кнопка 'Скрин'
    dp.callback_query.register(text_url, F.data.startswith('Текст'))  # Inline кнопка 'Текст'

    logging.basicConfig(level=logging.INFO)  # Настраиваем логирование (необходимо для отслеживания действий)

    try:
        await dp.start_polling(bot)  # Запускаем бота на прослушивание входящих сообщений
    finally:
        await bot.session.close()


# Основной запуск
if __name__ == '__main__':
    asyncio.run(start())
