from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_DELETE_KB


def create_delete_users_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_DELETE_KB[button] if button in LEXICON_DELETE_KB else button,
        callback_data=button) for button in buttons], width=2)
    return kb_builder.as_markup()
