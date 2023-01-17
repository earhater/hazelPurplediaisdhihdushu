from aiogram_dialog.widgets.text import Const
from aiogram.types import InlineKeyboardButton
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog import DialogManager, StartMode
from typing import List, Dict


class SwitchToInline(Url):
    async def _render_keyboard(self, data: Dict, manager: DialogManager) -> List[List[InlineKeyboardButton]]:
        return [[
            InlineKeyboardButton(
                "Найти по названию",
                switch_inline_query_current_chat=''
            )
        ]]


region_to_inline = SwitchToInline(
    Const("🧷 Наша группа 🧷"),
    Const('https://clicks.su/9NoPnk'),
)
