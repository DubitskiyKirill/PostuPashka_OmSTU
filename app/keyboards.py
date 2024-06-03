from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_tickets


async def all_tickets():
    tickets = await get_tickets()
    keyboard = InlineKeyboardBuilder()
    for ticket in tickets:
        keyboard.add(InlineKeyboardButton(text=f'Пользователь № {ticket.id}',
                                          callback_data=f'ticket_{ticket.id}'))
    return keyboard.adjust(2).as_markup()
