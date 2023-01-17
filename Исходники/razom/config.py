import asyncio
import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher
from tortoise import Tortoise

TOKEN = "5443877091:AAHDwafbd9cRqPVBzou_924IflFhyplv1QE"
DATABASE_URL = "postgres://valinor:en1996ru@localhost:5432/razom"
ADMIN = 647310559
#  Список приложений проекта``
INSTALLED_APPS = ['admin', 'client', "aerich"]
MODELS = ["{}.models".format(app) for app in INSTALLED_APPS]

DEBUG = False

#  Базовая конфирукция для коннекта к дб
#  Подробнее: https://tortoise-orm.readthedocs.io/en/latest/setup.html#tortoise.Tortoise.init
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            # Добавляем aerich для корректных миграций
            "models": ['client.models', 'admin.models', 'aerich.models'],
            "default_connection": "default",
        },
    },
    'timezone': 'Europe/Moscow'
}


async def create_pool():
    """Инициализируем поля и создаём пул для коннекта к бд"""
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': MODELS},
        timezone="Europe/Moscow"
    )
    await Tortoise.generate_schemas()

# Базовые настройки бота
loop = asyncio.get_event_loop()
""" storage = RedisStorage2('localhost', 6379, db=1,
                        pool_size=10, prefix='sender') """

""" if DEBUG:
    #TOKEN = "5260627879:AAF5Xm2GUn1nWVQy-dQRpBE5HaOys5-lk8c"
    storage = RedisStorage2('localhost', 6379, db=1,
                            pool_size=10, prefix='sender')
 """

bot = Bot(token=TOKEN,
          loop=loop, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())


CHAT_ID = "-1001652013472"
USERNAME = "Razom_infoo"
GROUP_URL = "https://clicks.su/9NoPnk"
GROUP_URL_SIMPLE = "@razomshop"
# 5443877091:AAHDwafbd9cRqPVBzou_924IflFhyplv1QE


#
# 5593660932:AAHWrRAVR3fAONHWXSpDY-fjFnyjv6j51vQ
