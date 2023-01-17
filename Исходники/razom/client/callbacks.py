from typing import Dict

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram_dialog import DialogManager, StartMode
from client.states import BaseClientCabinetState
from config import ADMIN, bot, dp
from loguru import logger

to_menu = CallbackData('menu', 'action')


@dp.callback_query_handler(to_menu.filter(action=['to_menu']))
async def start_base_client_dialog(query: types.CallbackQuery, callback_data: Dict[str, str],  dialog_manager: DialogManager):
    await bot.delete_message(query.from_user.id, message_id=query.message.message_id)
    await dialog_manager.start(BaseClientCabinetState.base_state, mode=StartMode.RESET_STACK)
