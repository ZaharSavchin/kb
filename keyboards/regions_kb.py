from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_REGIONS


def create_regions_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON_REGIONS[button] if button in LEXICON_REGIONS else button,
        callback_data=button) for button in buttons], width=1)
    return kb_builder.as_markup()
