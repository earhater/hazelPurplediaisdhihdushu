from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminState(StatesGroup):
    base_state = State()
    moderation = State()
    income = State()

    catalog = State()
    show_single_catalog_item = State()
    edit_single_catalog_item = State()
    add_link_catalog = State()

    present = State()
    show_single_present_item = State()
    edit_single_present_item = State()
    add_link_present = State()

    config = State()
    config_terms = State()
