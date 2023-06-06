from aiogram.types import Message


# В этом файле хранятся ответы на команды

# Команда /start
async def start_command(message: Message):
    await message.answer('Отправьте ссылку')  # Отправляем сообщение пользователю
