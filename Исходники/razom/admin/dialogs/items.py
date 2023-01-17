import re
from operator import itemgetter

from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaPhoto, Message)
from aiogram.utils.callback_data import CallbackData
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.kbd import (Button, Column, ManagedCheckboxAdapter,
                                        Radio, ScrollingGroup, Select)
from aiogram_dialog.widgets.text import Format
from config import bot
from loguru import logger

from ..models import Catalog, Config, Present
from ..states import AdminState
from .moderation import get_moderation_photo


async def on_cat_item_click(
    c: CallbackQuery, button: Button, manager: DialogManager, item_id: str
) -> None:
    catalog_item = await Catalog.get(id=item_id)
    await manager.update({
        "cat_item_edit": item_id,
        "cat_item_text": catalog_item.text,
        'cat_item_url': catalog_item.link
    })

    await manager.dialog().switch_to(AdminState.show_single_catalog_item)


catalog_l = Column(Select(
    Format("{item[0]}"),
    id="cat_adm",
    item_id_getter=itemgetter(1),
    items="catalog_items",
    on_click=on_cat_item_click,
)
)


async def edit_single_catalog_item(query: CallbackQuery, button: Button, manager: DialogManager):
    logger.debug("edit")


async def precess_new_catalog_item_data(message: Message, button: Button, manager: DialogManager):
    dialog_data = manager.current_context().dialog_data
    text, link = message.text.split(" ")
    if "https" not in link:
        await message.reply("Вторым параметром должна идти ссылка, пример:\n сбермаркет https://market.sber.ru/")
        return
    if len(text) > 25:
        await message.reply("Длина текста для кнопки не должна превышать 25 символов, пример:\n сбермаркет https://market.sber.ru/")
        return
    await Catalog.filter(id=dialog_data['cat_item_edit']).update(link=link.strip(), text=text.strip())
    await manager.dialog().switch_to(AdminState.catalog)


async def precess_new_catalog_item(message: Message, button: Button, manager: DialogManager):
    dialog_data = manager.current_context().dialog_data
    text, link = message.text.split(",")
    if "https" not in link:
        await message.reply("Вторым параметром должна идти ссылка, пример:\n сбермаркет https://market.sber.ru/")
        return
    if len(text) > 25:
        await message.reply("Длина текста для кнопки не должна превышать 25 символов, пример:\n сбермаркет https://market.sber.ru/")
        return
    await Catalog.create(link=link.strip(), text=text.strip())
    await manager.dialog().switch_to(AdminState.catalog)


# PRESENT ========
async def precess_new_present_item_data(message: Message, button: Button, manager: DialogManager):
    dialog_data = manager.current_context().dialog_data
    text, link = message.text.split(" ")
    if "https" not in link:
        await message.reply("Вторым параметром должна идти ссылка, пример:\n сбермаркет https://market.sber.ru/")
        return
    if len(text) > 25:
        await message.reply("Длина текста для кнопки не должна превышать 25 символов, пример:\n сбермаркет https://market.sber.ru/")
        return
    await Present.filter(id=dialog_data['pres_item_edit']).update(link=link.strip(), title=text.strip())
    await manager.dialog().switch_to(AdminState.present)


async def precess_new_present_item(message: Message, button: Button, manager: DialogManager):
    dialog_data = manager.current_context().dialog_data
    text, link = message.text.split(",")
    if "https" not in link:
        await message.reply("Вторым параметром должна идти ссылка, пример:\n сбермаркет https://market.sber.ru/")
        return
    if len(text) > 25:
        await message.reply("Длина текста для кнопки не должна превышать 25 символов, пример:\n сбермаркет https://market.sber.ru/")
        return
    await Present.create(link=link.strip(), title=text.strip())
    await manager.dialog().switch_to(AdminState.present)


async def on_present_elem_click(
    c: CallbackQuery, button: Button, manager: DialogManager, item_id: str
) -> None:
    logger.debug(item_id)
    present_item = await Present.get(id=item_id)
    await manager.update({
        "pres_item_edit": item_id,
        "pres_item_text": present_item.title,
        'pres_item_url': present_item.link
    })

    await manager.dialog().switch_to(AdminState.show_single_present_item)

present_l = Column(Select(
    Format("{item[0]}"),
    id="pres_adm",
    item_id_getter=itemgetter(1),
    items="present_items",
    on_click=on_present_elem_click,
)
)


# ======= CONFIG

async def process_new_terms_text(message: Message, button: Button, manager: DialogManager):
    await manager.update({'terms': message.text})
    await Config.filter(id=1).update(terms=message.text)
    await manager.dialog().switch_to(AdminState.config)


async def delete_element(query: CallbackQuery, button: Button, manager: DialogManager):
    dialog_data = manager.current_context().dialog_data

    if button.widget_id == "delete_cat_elem":
        await Catalog.filter(id=dialog_data['cat_item_edit']).delete()
        catalog_items = await Catalog.all()
        await manager.update({"catalog_items": [(f"{x.text}", x.pk) for x in catalog_items], })
        await query.message.reply("✅ Элемент успешно удалён")
        await manager.dialog().switch_to(AdminState.catalog)
        return
    if button.widget_id == "delete_pres_elem":
        await Present.filter(id=dialog_data['pres_item_edit']).delete()
        present_items = await Present.all()
        await manager.update({"present_items": [(f"{x.title}", x.pk) for x in present_items]})
        await query.message.reply("✅ Элемент успешно удалён")
        await manager.dialog().switch_to(AdminState.present)
        return

extended_paginator_cb = CallbackData("base_paginator", 'page', 'action')
single_photo = CallbackData('client_post', 'action', 'id')


async def open_moderation(query: CallbackQuery, button: Button, manager: DialogManager):
    photo, markup = await get_moderation_photo(page=1)
    logger.debug(photo)
    await bot.send_photo(query.from_user.id, photo=photo, reply_markup=markup)
