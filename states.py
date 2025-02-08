from aiogram.fsm.state import State, StatesGroup


class Menus(StatesGroup):
    destiny=State()
    main_menu=State()
    prompt = State()
    image = State()
    art = State()
    art_prompt=State()
