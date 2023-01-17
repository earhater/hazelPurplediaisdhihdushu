from typing import Dict

from admin.models import Catalog, Config, Present
from admin.states import AdminState
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (Back, Button, Checkbox, Column,
                                        ListGroup, ManagedCheckboxAdapter,
                                        ManagedListGroupAdapter, Radio, Row,
                                        SwitchTo, Url)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from loguru import logger

from .items import (catalog_l, delete_element, edit_single_catalog_item,
                    open_moderation, precess_new_catalog_item,
                    precess_new_catalog_item_data, precess_new_present_item,
                    precess_new_present_item_data, present_l,
                    process_new_terms_text)

TERMS = "<b>✔️ Условия розыгрыша:</b>\nПриобретая наши товары, вы становитесь участником постоянного розыгрыша <b>ЦЕННОГО ПРИЗА - 🤗 </b>\n"\
    "Выполнив условия, вы получаете свой постоянный номер и каждый месяц участвуете в розыгрыше."\
    "А это значит, что вы можете стать победителям несколько раз." \
    "Желаем вам удачи!"

# https://api.telegram.org/bot5443877091:AAHDwafbd9cRqPVBzou_924IflFhyplv1QE/getUpdates


async def base_menu_getter(dialog_manager: DialogManager, **kwargs):
    await Config.get_or_create(id=1, defaults={'terms': TERMS, 'group': 'https://valinor.ru/'})
    config_data = await Config.get(id=1)
    dialog_data = dialog_manager.current_context().dialog_data

    catalog_items = await Catalog.all()

    present_items = await Present.all()

    return {
        "catalog_items": [(f"{x.text}", x.pk) for x in catalog_items],
        "cat_item_edit": dialog_data.get("cat_item_edit", None),
        "cat_item_text": dialog_data.get("cat_item_text", None),
        "cat_item_url": dialog_data.get("cat_item_url", None),

        "present_items": [(f"{x.title}", x.pk) for x in present_items],
        "pres_item_edit": dialog_data.get("pres_item_edit", None),
        "pres_item_text": dialog_data.get("pres_item_text", None),
        "pres_item_url": dialog_data.get("pres_item_url", None),


        "terms": config_data.terms


    }
""" SwitchTo(Const("♻️ Фото на модерации"), id="on_moder",
                 state=AdminState.moderation), """

""" SwitchTo(Const("✉️ Входящие сообщения"), id="income_msg",
                 state=AdminState.income), """
AdminDialog = Dialog(
    Window(
        Format("Добро пожаловать в админ панель"),
        SwitchTo(Const("⚙️ Базовые настройки"), id="settings",
                 state=AdminState.config),
        Button(Const("♻️ Фото на модерации"),
               id="on_moder", on_click=open_moderation),

        SwitchTo(Const("🔖 Каталог"), id="catal",
                 state=AdminState.catalog),
        SwitchTo(Const("🎁 Подарки"), id="prese",
                 state=AdminState.present),

        state=AdminState.base_state,
        getter=base_menu_getter,
    ),


    Window(

        Format("Модерация"),

        Back(Const("↩️ Назад")),
        state=AdminState.moderation,
        getter=base_menu_getter,
    ),

    Window(

        Format("Входящие сообщения"),
        Back(Const("↩️ Назад")),
        state=AdminState.income,
        getter=base_menu_getter,
    ),

    Window(
        Format("Каталог"),
        catalog_l,
        SwitchTo(Const("➕ Добавить каталог"), id="catal",
                 state=AdminState.add_link_catalog),

        SwitchTo(Const("↩️ Назад"), id="prese",
                 state=AdminState.base_state),

        state=AdminState.catalog,
        getter=base_menu_getter,
    ),

    Window(
        Const("Редактирование элемента каталога"),
        Format("Текст кнопки: <b>{cat_item_text}</b>"),
        Format("Текст кнопки: {cat_item_url}"),

        SwitchTo(Const("✏️ Редактироват"), id="edit_single_catalog",
                 state=AdminState.edit_single_catalog_item),
        Button(Const("❌ Удалить"), id="delete_cat_elem",
               on_click=delete_element),



        SwitchTo(Const("↩️ Назад"), id="prese",
                 state=AdminState.catalog),
        state=AdminState.show_single_catalog_item,
        getter=base_menu_getter,
        disable_web_page_preview=True
    ),

    Window(
        Const("<b>Укажите новые данные в формате текст ссылка</b>"),
        MessageInput(precess_new_catalog_item_data),
        SwitchTo(Const("↩️ Назад"), id="prese",
                 state=AdminState.show_single_catalog_item),
        state=AdminState.edit_single_catalog_item,
        getter=base_menu_getter,
        disable_web_page_preview=True
    ),

    Window(
        Const("<b>Укажите данные в формате текст ссылка</b>"),
        MessageInput(precess_new_catalog_item),
        SwitchTo(Const("↩️ Назад"), id="prese",
                 state=AdminState.catalog),
        state=AdminState.add_link_catalog,
        getter=base_menu_getter,
        disable_web_page_preview=True
    ),

    # =============== present =================
    Window(
        Format("Подарки"),
        present_l,
        SwitchTo(Const("➕ Добавить подарок"), id="catal",
                 state=AdminState.add_link_present),
        SwitchTo(Const("↩️ Назад"), id="prese",
                 state=AdminState.base_state),
        state=AdminState.present,
        getter=base_menu_getter,
    ),

    Window(
        Const("Редактирование элемента"),
        Format("Текст кнопки: <b>{pres_item_text}</b>"),
        Format("Текст кнопки: {pres_item_url}"),

        SwitchTo(Const("✏️ Редактировать"), id="edit_single_catalog",
                 state=AdminState.edit_single_present_item),
        Button(Const("❌ Удалить"), id="delete_pres_elem",
               on_click=delete_element),


        SwitchTo(Const("↩️ Назад"), id="bb",
                 state=AdminState.present),
        state=AdminState.show_single_present_item,
        getter=base_menu_getter,
        disable_web_page_preview=True
    ),

    Window(
        Const("<b>Укажите новые данные в формате текст ссылка</b>"),
        MessageInput(precess_new_present_item_data),
        SwitchTo(Const("↩️ Назад"), id="prese",
                 state=AdminState.show_single_present_item),
        state=AdminState.edit_single_present_item,
        getter=base_menu_getter,
        disable_web_page_preview=True
    ),

    Window(
        Const("<b>Укажите данные в формате текст ссылка</b>"),
        MessageInput(precess_new_present_item),
        SwitchTo(Const("↩️ Назад"), id="bb",
                 state=AdminState.present),
        state=AdminState.add_link_present,
        getter=base_menu_getter,
        disable_web_page_preview=True
    ),



    Window(
        Format("Настройки"),
        SwitchTo(Const("✏️ Условия розыгрыша"), id="edit_terms",
                 state=AdminState.config_terms),
        SwitchTo(Const("↩️ Назад"), id="bc",
                 state=AdminState.base_state),
        state=AdminState.config,
        getter=base_menu_getter,
    ),

    Window(
        Format("{terms}"),
        MessageInput(process_new_terms_text),
        Back(Const("↩️ Назад")),
        state=AdminState.config_terms,
        getter=base_menu_getter,
    ),

)
