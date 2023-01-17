from typing import List, Optional, Union

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from client.models import Moderation
from loguru import logger

from .pagination import PaginatorExtended

extended_paginator_cb = CallbackData("base_paginator", 'page', 'action')
single_photo = CallbackData('client_post', 'action', 'id')

# :


# -> Union[str, InlineKeyboardMarkup]:

async def split_list(the_list: list, chunk_size: int) -> List:
    """split list for paginator"""
    result_list = []
    while the_list:
        result_list.append(the_list[:chunk_size])
        the_list = the_list[chunk_size:]
    return result_list


async def get_post_logs() -> Optional[list]:
    """Получаем все логи по рассылке"""
    all_logs = await Moderation.filter(accepted=False).order_by('-created_at')
    paginated_logs = await split_list(all_logs, 1)
    if len(paginated_logs) >= 1:
        return paginated_logs


async def get_moderation_photo(page=1):
    # on_moderation = await Moderation.filter(accepted=False).values()
    on_moderation = await get_post_logs()

    paginator = PaginatorExtended(
        page_count=len(on_moderation),
        current_page=int(page),
        action="moderaion_nav"
    )
    photo = on_moderation[page-1][0].image
    client_id = on_moderation[page-1][0].user_id

    """ for item in on_moderation[page-1].items():
        
        logger.debug(item) """
    paginator.add_before(
        InlineKeyboardButton(
            "✅ Принять",
            callback_data=single_photo.new(
                action='accept_moder',
                id=client_id)),
        InlineKeyboardButton(
            "❌ Отклонить",
            callback_data=single_photo.new(
                action='dec_moder',
                id=client_id))
    )

    return photo, paginator.markup
