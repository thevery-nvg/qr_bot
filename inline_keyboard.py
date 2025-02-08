from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

FIRST = "#fisrst#"
SECOND = "#second#"

first_btn = [InlineKeyboardButton(text="Первый вариант", callback_data=FIRST)]
second_btn = [InlineKeyboardButton(text="Второй вариант", callback_data=SECOND)]


def main_kbd():
    return InlineKeyboardMarkup(inline_keyboard=[first_btn,
                                                 second_btn])
