from aiogram.fsm.state import StatesGroup, State


class AddToken(StatesGroup):
    token = State()
    reset_token = State()
