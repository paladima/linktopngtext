from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os.path import abspath
from os import remove
import asyncio

from linktopngtext.core.utils.statesform import StepsForm


async def screen_url(call: CallbackQuery, bot: Bot):
    await call.message.answer('Идет загрузка...')

    # Получение ссылки
    url_number_data = call.data.split("_", 1)[1]
    try:
        url = StepsForm.url_number[int(url_number_data)]
    except IndexError:
        await call.message.answer(text='Отправьте ссылку снова')

    # Скрываем графический интерфейс
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # Инициация драйвера Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # Загрузка страницы
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, driver.get, url)

    # Получение размеров страницы
    page_width = await loop.run_in_executor(None, driver.execute_script, "return document.body.scrollWidth")
    page_height = await loop.run_in_executor(None, driver.execute_script, "return document.body.scrollHeight")

    driver.set_window_size(width=page_width, height=page_height)  # Размеры страницы

    await asyncio.sleep(7)  # Прогрузка страницы перед скриншотом

    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Отправка скриншота')

    # Сохранение скриншота
    await loop.run_in_executor(None, driver.save_screenshot, 'core/files_to_send/{}.png'.format(call.message.chat.id))

    # Закрываем драйвер
    driver.quit()

    await send_screenshot(call, bot, url)


# Отправка скриншота
async def send_screenshot(call: CallbackQuery, bot: Bot, url):
    # Получение файла
    document_file = 'core/files_to_send/{}.png'.format(call.message.chat.id)
    document_path = abspath(document_file)
    document = FSInputFile(document_path)
    await bot.send_document(chat_id=call.message.chat.id, document=document, caption='Скриншот: ' + url)

    # Удаление файла

    remove(document_path)
    # remove('core/files_to_send/{}.png'.format(call.message.chat.id))
