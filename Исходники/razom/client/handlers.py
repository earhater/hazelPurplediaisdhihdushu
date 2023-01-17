import hashlib

from admin.states import AdminState
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from client.models import Client
from client.states import BaseClientCabinetState
from config import bot, dp
from loguru import logger


@dp.message_handler(commands=['start'])
async def cmd_start(message: Message, dialog_manager: DialogManager):
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    await Client.get_or_create(telegram_id=message.from_user.id, defaults={'telegram_username': username})
    await dialog_manager.start(BaseClientCabinetState.base_state, mode=StartMode.RESET_STACK)


@dp.message_handler(commands=['admin'])
async def cmd_admin(message: Message, dialog_manager: DialogManager):
    if message.from_user.id in [647310559, 5277062568]:
        await dialog_manager.start(AdminState.base_state, mode=StartMode.RESET_STACK)

    """ username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    await Client.get_or_create(telegram_id=message.from_user.id, defaults={'telegram_username': username})
    await dialog_manager.start(BaseClientCabinetState.base_state, mode=StartMode.RESET_STACK) """
