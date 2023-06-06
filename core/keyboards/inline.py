from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание кнопок
def inline_button(url_number: str | int):
    inline = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Скриншот',
                callback_data='Скриншот_' + str(url_number)
            )
        ],
        [
            InlineKeyboardButton(
                text='Текст',
                callback_data='Текст_' + str(url_number)
            )
        ]
    ])
    return inline
