import asyncio
import logging

from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.token import BOT_TOKEN
from handlers.main.coefficients import CoefficientsHandler
from handlers.main.main import MainHandler
from handlers.main.state_list import StateHandler
from handlers.start.start import StartHandler
from services.check_token import CheckToken
from services.check_stocks import CheckStocks
from services.coefficients import CheckCoef
from services.incomes import CheckState
from db.db import Db


class MainBot:
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.db = Db(db_name="freelance.db")
        self.start_handler = StartHandler(db=self.db, check_token=CheckToken)
        self.main_handler = MainHandler(db=self.db, check_stocks=CheckStocks)
        self.state_list = StateHandler(db=self.db, check_incomes=CheckState)
        self.coef = CoefficientsHandler(db=self.db, check_coef=CheckCoef)
        self.setup()

    def setup(self):
        self.dp.include_routers(*[self.start_handler.router,
                                  self.main_handler.router,
                                  self.state_list.router,
                                  self.coef.router])
        self.dp.message.middleware(ChatActionMiddleware())

    async def start(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot, allowed_updates=self.dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main_bot = MainBot(BOT_TOKEN)
    asyncio.run(main_bot.start())
