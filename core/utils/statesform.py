from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    '''Машина состояний'''
    GET_URL = State()  # Сначала хотел сделать бота через FSM, но потом передумал (ненужная строка)
    url_number = []  # Используется для передачи url
