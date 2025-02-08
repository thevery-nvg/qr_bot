from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

FIRST = "#fisrst#"
SECOND = "#second#"

first_btn = [InlineKeyboardButton(text="Первый вариант", callback_data=FIRST)]
second_btn = [InlineKeyboardButton(text="Второй вариант", callback_data=SECOND)]


def main_kbd():
    return InlineKeyboardMarkup(inline_keyboard=[first_btn,
                                                 second_btn])


return_to_main_btn = [InlineKeyboardButton(text="return to main menu",
                                           callback_data="#main_menu_cb#")]




def return_to_main_kbd():
    return InlineKeyboardMarkup(inline_keyboard=[
        return_to_main_btn])
