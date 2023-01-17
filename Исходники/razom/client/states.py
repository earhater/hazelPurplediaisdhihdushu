from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseClientCabinetState(StatesGroup):
    base_state = State()
    presents_state = State()
    lotto_state = State()
    catalog_state = State()
    photo_state = State()
    question_state = State()

    terms_state = State()
