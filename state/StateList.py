from aiogram.fsm.state import StatesGroup, State


class StateState(StatesGroup):
    sale_state = State()
    order_state = State()