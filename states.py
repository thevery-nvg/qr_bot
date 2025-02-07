from aiogram.fsm.state import State, StatesGroup


class Menus(StatesGroup):
    main_menu=State()
    prompt = State()
    image = State()
