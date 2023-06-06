from aiogram.types import CallbackQuery, FSInputFile
from os.path import abspath
from os import remove
from aiogram import Bot
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import aiohttp

from linktopngtext.core.utils.statesform import StepsForm


async def text_url(call: CallbackQuery, bot: Bot):
    await call.message.answer(text='Отправка текста...')

    # Получение ссылки
    url_number_data = call.data.split("_", 1)
    url_number_data = url_number_data[1]
    try:
        url = StepsForm.url_number[int(url_number_data)]
    except IndexError:
        await call.message.answer(text='Отправьте ссылку снова')

    user_agent = UserAgent().random
    headers = {'user-agent': user_agent}

    # Ассинхронное получение html текста
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')
    soup = soup.find('body')

    # bs4 ищет эти теги
    text = soup.find_all(
        ['p', 'blockquote', 'code', 'b', 'i', 'u', 'strike', 'sup', 'sub', 'small', 'big', 'em', 'strong', 'pre',
         'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    empty_text = True  # Проверка на пустоту текста
    copyright_flag = False  # Проверка на '©' (Copyright)

    with open('core/files_to_send/{}.txt'.format(call.message.chat.id), 'w', encoding='utf-8') as file:
        for element in text:
            for symbol in element.get_text():
                if symbol == '©':
                    copyright_flag = True

            # Элемент страницы загружается если он не пустой и не содержит '©' (Copyright)
            if element.get_text().strip() != '' and copyright_flag is False:
                empty_text = False
                copyright_flag = False

                # Запись текста в файл
                file.write(element.get_text() + '\n')

    # Если текст пустой
    if empty_text:
        await call.message.answer(text='Упс... Похоже текст страницы пустой', parse_mode='HTML')
    else:
        await send_text(call, bot, url)


# Отправка текста
async def send_text(call: CallbackQuery, bot: Bot, url):
    # Получение файла
    document_file = 'core/files_to_send/{}.txt'.format(call.message.chat.id)
    document_path = abspath(document_file)
    document = FSInputFile(document_path)

    await bot.send_document(chat_id=call.message.chat.id, document=document, caption='Текст: ' + url)

    # Удаление файла
    remove(document_path)
