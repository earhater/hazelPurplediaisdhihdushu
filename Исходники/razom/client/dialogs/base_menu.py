from typing import Dict

from admin.models import Config
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (Back, Button, Checkbox, Column,
                                        ListGroup, ManagedCheckboxAdapter,
                                        Radio, Row, SwitchTo, Url)
from aiogram_dialog.widgets.text import Const, Format
from client.models import Client
from client.states import BaseClientCabinetState
from config import CHAT_ID, GROUP_URL, GROUP_URL_SIMPLE, USERNAME, bot
from loguru import logger

from .items import (catalog, our_group, precess_photo, present,
                    process_edit_user_info, render_catalog, render_present)

TERMS = "<b>✔️ Условия розыгрыша:</b>\nПриобретая наши товары, вы становитесь участником постоянного розыгрыша <b>ЦЕННОГО ПРИЗА - 🤗 </b>\n"\
    "Выполнив условия, вы получаете свой постоянный номер и каждый месяц участвуете в розыгрыше."\
    "А это значит, что вы можете стать победителям несколько раз." \
    "Желаем вам удачи!"


async def base_menu_getter(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.current_context().dialog_data
    additional_info = "✅ Вы подписаны на нашу группу, не забудьте отправить фото отзыва через рездел 'Розыгрыш'"
    user_info = await Client.get(telegram_id=dialog_manager.event.from_user.id)
    await Client.filter(telegram_id=dialog_manager.event.from_user.id).update(is_participating=True)
    try:
        is_ = await bot.get_chat_member(chat_id=CHAT_ID, user_id=dialog_manager.event.from_user.id)
        if is_['status'] == 'left':
            additional_info = "❕ Вы не подписаны на нашу группу, для участия в розыгрыше нужно быть подписаным на нашу группу @razomshop и загрузить фото Вашего отзыва для модерации"
            await Client.filter(telegram_id=dialog_manager.event.from_user.id).update(is_participating=False)
    except Exception as e:
        await Client.filter(telegram_id=dialog_manager.event.from_user.id).update(is_participating=False)
        additional_info = f"❕ Вы не подписаны на нашу группу, для участия в розыгрыше нужно быть подписаным на нашу группу {GROUP_URL_SIMPLE} и загрузить фото Вашего отзыва для модерации"

    user_info = await Client.get(telegram_id=dialog_manager.event.from_user.id)
    additional_info = "❕"
    if user_info.is_participating and user_info.moderation_accept:
        user_info.generate_personal_number()
        await user_info.save()
        logger.debug(user_info.personal_number)
        additional_info = "<b>✅ Вы участвуете в розыгрыше 👍</b>"

    else:
        user_info = await Client.get(telegram_id=dialog_manager.event.from_user.id)
        if not user_info.is_participating:
            additional_info += "Вы не подписаны на нашу группу @razomshop\n"
        if not user_info.moderation_accept:
            additional_info += "Ваше фото пока не прошло модерацию или Вы его не загрузили"

    config_data = await Config.get(id=1)

    return {
        "name": "alex",
        "personal_number": str(user_info.personal_number).replace("None", "-"),
        "terms": config_data.terms,
        "in_group": additional_info
    }


async def on_menu_element_click(query: CallbackQuery, button: Button, manager: DialogManager):

    if button.widget_id == "catal":
        catalog = await render_catalog()
        await manager.done()
        await query.message.reply("Наш каталог", reply_markup=catalog)
    elif button.widget_id == "prese":
        present = await render_present()
        await manager.done()
        await query.message.reply("Подарки для Вас", reply_markup=present)


ShowSearchMenu = Dialog(
    Window(
        Format("<b>Добрый день {name} </b>"),
        Format("Персональный номер для розыгрыша: {personal_number}"),
        Format("{in_group}"),
        Const("Выбирете раздел:"),
        Column(




            Button(Const('🎁 Получить подарки 🎁'),
                   on_click=on_menu_element_click, id='prese'),

            SwitchTo(Const("💎 Розыгрыш 💎"), id="lotto",
                     state=BaseClientCabinetState.lotto_state),
        ),
        Row(
            Button(Const('🔖 Наш каталог 🔖'),
                   on_click=on_menu_element_click, id='catal'),



            Url(
                Const("🧷 Наша группа 🧷"),
                Const(f'{GROUP_URL}'),
            )
        ),
        Url(
            Const("Есть ворос ❓"),
            Const(f'https://t.me/{USERNAME}'),
        ),




        state=BaseClientCabinetState.base_state,
        getter=base_menu_getter,
    ),

    Window(

        Const("\n<b>Подарки от нашей компании</b>"),



        Url(
            Const("Получить подарки от нашей компании"),
            Const('https://t.me/+phQslHnJ0WA0NTMy'),
        ),

        SwitchTo(Const("↩️ В меню"), id="to_menu",
                 state=BaseClientCabinetState.base_state),
        state=BaseClientCabinetState.presents_state,
        getter=base_menu_getter,
    ),

    Window(

        Format("{terms}"),
        Column(


            SwitchTo(Const("✅ Принять участие"), id="to_menu",
                     state=BaseClientCabinetState.photo_state),
        ),
        SwitchTo(Const("↩️ В меню"), id="m",
                 state=BaseClientCabinetState.base_state),


        state=BaseClientCabinetState.lotto_state,
        getter=base_menu_getter,
    ),

    Window(

        Const("<b>Не забудьте подписаться на нашу группу @razomshop\nОтправьте фото Вашего отзыва на сайте wildberries</b>"),
        MessageInput(precess_photo,
                     content_types=types.ContentTypes.PHOTO),


        SwitchTo(Const("↩️ Назад"), id="to_",
                 state=BaseClientCabinetState.lotto_state),
        state=BaseClientCabinetState.photo_state,
        getter=base_menu_getter,
    ),


    Window(

        Const("<b>Выберите удобный для Вас магазин:</b>"),
        catalog,
        SwitchTo(Const("↩️ В меню"), id="to_menu",
                 state=BaseClientCabinetState.base_state),


        state=BaseClientCabinetState.catalog_state,
        getter=base_menu_getter,
    ),

    Window(

        Const("<b>Напишите свой вопрос, вы ответим в ближайшее время (не больше 1024 символов)</b>"),
        MessageInput(process_edit_user_info),
        SwitchTo(Const("↩️ В меню"), id="to_menu",
                 state=BaseClientCabinetState.base_state),
        state=BaseClientCabinetState.question_state,
        getter=base_menu_getter,
    ),
    Window(
        Format("{terms}"),

        SwitchTo(Const("↩️ Назад"), id="to_menu",
                 state=BaseClientCabinetState.lotto_state),
        state=BaseClientCabinetState.terms_state,
        getter=base_menu_getter,
    ),
)
