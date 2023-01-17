from admin import callbacks
from admin.dialogs.base import AdminDialog
from aiogram.utils import executor
from aiogram_dialog import DialogRegistry
from client import callbacks, handlers
from client.dialogs.base_menu import ShowSearchMenu
from config import create_pool, dp, loop

if __name__ == '__main__':
    loop.run_until_complete(create_pool())
    registry = DialogRegistry(dp)
    registry.register(ShowSearchMenu)
    registry.register(AdminDialog)

    executor.start_polling(dp, skip_updates=True)
