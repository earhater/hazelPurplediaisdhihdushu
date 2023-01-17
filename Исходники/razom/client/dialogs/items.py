# -*- coding: UTF-8 -*-
import asyncio
import operator
from operator import itemgetter

from admin.models import Catalog, Income, Present
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaPhoto, Message)
from aiogram.utils.callback_data import CallbackData
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import (Button, Column, ManagedCheckboxAdapter,
                                        Multiselect, Radio, ScrollingGroup,
                                        Select, Url)
from aiogram_dialog.widgets.text import Const, Format
from client.models import Client, Moderation
from client.states import BaseClientCabinetState
from config import bot
from loguru import logger

to_menu = CallbackData('menu', 'action')


async def nav_to(c: CallbackQuery, button: Button, manager: DialogManager, item_id):
    await c.answer()
    logger.debug("was clicked")

present = Column(Select(
    Format("{item[0]}"),
    id="r",
    item_id_getter=operator.itemgetter(1),
    items="presents",
    on_click=nav_to,
))


our_group = Url(
    Const("🧷 Наша группа 🧷"),
    Const('https://clicks.su/9NoPnk'),
)


catalog = Column(
    Url(
        Const("WildBerries"),
        Const('https://www.wildberries.ru/seller/214873'),
    ),
    Url(
        Const("OZON"),
        Const('https://www.ozon.ru/seller/razom-shop-262690/products/?miniapp=seller_262690'),
    ),
    Url(
        Const("Яндекс Маркет"),
        Const('https://market.yandex.ru/search?businessId=27261819&allowCollapsing=1&local-offers-first=1'),
    ),
    Url(
        Const("СберМегаМаркет"),
        Const('https://clicks.su/ydLbQZ'),
    )

)


async def process_edit_user_info(
        message: Message, button: Button, manager: DialogManager):
    if len(message.text) <= 1024:
        await Income.create(text=message.text, from_user=message.from_user.id)
        await message.reply("<b>✅ Спасибо за Ваше обращение, мы свяжимся с Вами в ближайшее время</b>")
        await manager.dialog().switch_to(BaseClientCabinetState.base_state)
        return
    else:
        await message.reply("❗ Длина сообщения не должна превышать 1024 символов")
        return


async def precess_photo(
        message: InputMediaPhoto, button: Button, manager: DialogManager):

    await Moderation.update_or_create(user_id=message.from_user.id, defaults={'image': f"{message['photo'][0]['file_id']}",  "accepted": False})
    await Client.filter(telegram_id=message.from_user.id).update(moderation_accept=False)
    additional_info = "✅ Вы подписаны на нашу группу, если фото пройдет модерацию, то Вы автоматически учавствуете в розыгрыше"
    try:

        is_ = await bot.get_chat_member(chat_id="-1001808624820", user_id=manager.event.from_user.id)
        if is_['status'] == 'left':
            additional_info = "❕ Вы не подписаны на нашу группу, для участия нужно быть подписаным."

    except:
        additional_info = "❕ Вы не подписаны на нашу группу, для участия нужно быть подписаным."

    await message.reply(f"<b>✅ Спасибо за участие, в ближайшее время мы рассмотрим Вашу заявку</b>\n{additional_info}")
    logger.debug(message['photo'][0])
    await manager.dialog().switch_to(BaseClientCabinetState.base_state)
    return


async def render_catalog():
    # await Catalog.create(text="item1", link="https://valinor.ru/")
    # await Catalog.create(text="item2", link="https://valinor2.ru/")
    all_links = await Catalog.all()
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = list()
    for i in all_links:
        buttons.append(InlineKeyboardButton(text=i.text, url=i.link))
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(
        "↩️ В меню", callback_data=to_menu.new(
            action='to_menu',
        )))
    return keyboard


async def render_present():
    all_links = await Present.all()
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = list()
    for i in all_links:
        buttons.append(InlineKeyboardButton(text=i.title, url=i.link))
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(
        "↩️ В меню", callback_data=to_menu.new(
            action='to_menu',
        )))
    return keyboard
