
from typing import Dict

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.utils.callback_data import CallbackData
from aiogram_dialog import DialogManager, StartMode
from client.models import Client, Moderation
from client.states import BaseClientCabinetState
from config import ADMIN, bot, dp
from loguru import logger

from .dialogs.moderation import get_moderation_photo

single_photo = CallbackData('client_post', 'action', 'id')
extended_paginator_cb = CallbackData("base_paginator", 'page', 'action')


async def send_notification_to_user(user_id: int, status: bool):
    if status:
        await bot.send_message(user_id, "✅ Ваше Фото успешно прошло модерацию, не забудьте подписаться на нашу группу @razomshop если еще не сделалили этого")
    else:
        await bot.send_message(user_id, "😔 К сожалению Ваше фото не прошло модерацию, убедитесь что вы отправили правильное фото, отправьте фото снова через раздел 'Розыгрыш'")


@dp.callback_query_handler(extended_paginator_cb.filter(action=['moderaion_nav']))
async def nav_between_moderation_image(query: types.CallbackQuery, callback_data: Dict[str, str]):
    logger.debug("NAVIGATWAERSD")

    await bot.delete_message(query.from_user.id, message_id=query.message.message_id)
    logger.debug(callback_data['page'])

    photo, markup = await get_moderation_photo(page=int(callback_data['page']))
    await bot.send_photo(query.from_user.id, photo=photo, reply_markup=markup)


@dp.callback_query_handler(single_photo.filter(action=['accept_moder', 'dec_moder']))
async def accept_or_decline_photo(query: types.CallbackQuery, callback_data: Dict[str, str]):
    if callback_data['action'] == "accept_moder":
        client = await Client.get(telegram_id=callback_data["id"])
        client.moderation_accept = True
        client.generate_personal_number()
        await client.save()
        await Moderation.filter(user_id=callback_data["id"]).delete()
        await bot.delete_message(query.from_user.id, message_id=query.message.message_id)
        await send_notification_to_user(int(callback_data["id"]), status=True)
        photo, markup = await get_moderation_photo(page=1)
        await bot.send_photo(query.from_user.id, photo=photo, reply_markup=markup)
    elif callback_data['action'] == "dec_moder":
        client = await Client.get(telegram_id=callback_data["id"])
        client.moderation_accept = False
        await client.save()
        await Moderation.filter(user_id=callback_data["id"]).delete()
        await bot.delete_message(query.from_user.id, message_id=query.message.message_id)
        await send_notification_to_user(int(callback_data["id"]), status=False)
        photo, markup = await get_moderation_photo(page=1)
        await bot.send_photo(query.from_user.id, photo=photo, reply_markup=markup)
