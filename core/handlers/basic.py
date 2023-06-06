from aiogram import Bot
from aiogram.types import Message
from fake_useragent import UserAgent
import requests
import re

from linktopngtext.core.utils.statesform import StepsForm
from linktopngtext.core.keyboards.inline import inline_button


# Является ли слово ссылкой (проверка)
def is_link(word) -> bool:
    pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*$'
    return not not (re.match(pattern, word))


# Обработка сообщения
async def get_url(message: Message, bot: Bot):
    url_bool = is_link(message.text)  # True или False
    if url_bool:  # Если текст пользователя - это ссылка

        try:
            user_agent = UserAgent().random
            headers = {'user-agent': user_agent}
            url = message.text
            response = requests.head(url, headers=headers, timeout=7)
            if response.status_code == 200:  # Если страница загрузилась
                await url_true(message, bot)
            else:  # Если страница не загрузилась
                await message.answer(
                    text="Не удалось открыть ссылку. Ошибка " + str(response.status_code))  # Отсылает номер ошибки

        except requests.exceptions.Timeout:
            await message.answer(
                text="Превышено время ожидания ответа от сервера")  # Если страница не загрузилась за 7 секунд

        except:
            await message.answer(text="Не удается открыть эту страницу")

    else:  # Если текст пользователя - это не ссылка
        await message.answer(text="Вы отправили не ссылку")


# Запускается если страница загрузилась
async def url_true(message: Message, bot: Bot):
    url = message.text
    StepsForm.url_number.append(url)
    number_url = StepsForm.url_number.index(url)
    await bot.send_message(
        chat_id=message.chat.id,
        text="Выберите вариант: вывод текста или отправка скриншота. Нажмите на соответсвующие кнопки",
        reply_markup=inline_button(number_url))