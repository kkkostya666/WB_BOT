import datetime
import re

from keyboards.start_keyboards import main_keyboard, time_keyboard
from aiogram import types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from state.date_state import DateState
from text.start.start import start_message
from aiogram import Router
from state.token import AddToken


class MainHandler:
    def __init__(self, db, check_stocks):
        self.router = Router()
        self.db = db
        self.check_stocks = check_stocks
        self.register_handlers()

    def register_handlers(self):
        self.router.callback_query(F.data == 'control_tovar')(self.control)
        self.router.callback_query(F.data == 'today')(self.today)
        self.router.callback_query(F.data == 'yesterday')(self.yesterday)
        self.router.callback_query(F.data == 'self_go')(self.self_go)
        self.router.message(DateState.date_state)(self.process_date)

    async def control(self, callback: types.CallbackQuery):
        await callback.message.answer(
            "Выберите или введите дату для получение информации о наличии товаров на момент введеной даты",
            reply_markup=await time_keyboard())

    async def today(self, callback: types.CallbackQuery):
        get_token = self.db.get_token_by_user_id(callback.from_user.id)

        today_date = datetime.datetime.now().strftime("%Y-%m-%d")

        result = self.check_stocks.check_stocks_get(auth_token=get_token, dateFrom=today_date)
        print(result)

        if result:
            for item in result:
                warehouse = item['warehouseName']
                quantity = item['quantity']
                in_way_to_client = item['inWayToClient']
                in_way_from_client = item['inWayFromClient']
                quantity_full = item['quantityFull']
                subject = item['subject']
                price = item['Price']
                discount = item['Discount']

                item_text = (
                    f"📦 Склад: {warehouse}\n"
                    f"📌 Наименование товара: {subject}\n"
                    f"📅 Количество: {quantity}\n"
                    f"🚚 В пути к клиенту: {in_way_to_client}\n"
                    f"🔄 В пути от клиента: {in_way_from_client}\n"
                    f"📊 Полное количество: {quantity_full}\n"
                    f"💵 Цена: {price}\n"
                    f"🎉 Скидка: {discount}%"
                )

                await callback.message.answer(item_text, parse_mode="Markdown")
        else:
            await callback.message.answer("Товары на сегодня не найдены.")
        await callback.message.answer(text="<b>Представлены все товары которые доступны на сегодня</b>",
                                      parse_mode="HTML",
                                      reply_markup=await main_keyboard())

    async def yesterday(self, callback: types.CallbackQuery):
        get_token = self.db.get_token_by_user_id(callback.from_user.id)

        yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        result = self.check_stocks.check_stocks_get(auth_token=get_token, dateFrom=yesterday_date)
        print(result)

        if result:
            for item in result:
                warehouse = item['warehouseName']
                quantity = item['quantity']
                in_way_to_client = item['inWayToClient']
                in_way_from_client = item['inWayFromClient']
                quantity_full = item['quantityFull']
                subject = item['subject']
                price = item['Price']
                discount = item['Discount']

                item_text = (
                    f"📦 Склад: {warehouse}\n"
                    f"📌 Наименование товара: {subject}\n"
                    f"📅 Количество: {quantity}\n"
                    f"🚚 В пути к клиенту: {in_way_to_client}\n"
                    f"🔄 В пути от клиента: {in_way_from_client}\n"
                    f"📊 Полное количество: {quantity_full}\n"
                    f"💵 Цена: {price}\n"
                    f"🎉 Скидка: {discount}%"
                )

                await callback.message.answer(item_text, parse_mode="Markdown")
        else:
            await callback.message.answer("Товары на сегодня не найдены.")
        await callback.message.answer(text="<b>Представлены все товары которые доступны за вчера</b>",
                                      parse_mode="HTML",
                                      reply_markup=await main_keyboard())

    async def self_go(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(text="Введите дату в формате 2020-11-11")
        await state.set_state(DateState.date_state)

    async def process_date(self, message: types.Message, state: FSMContext):
        # Check if the input is a valid date format
        date_text = message.text
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_text):
            await message.answer("❌ Пожалуйста, введите дату в формате YYYY-MM-DD.")
            return

        # Try parsing the date to ensure it's valid
        try:
            date_from = datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            await message.answer("❌ Неверный формат даты. Попробуйте снова.")
            return

        # Fetch user's token
        get_token = self.db.get_token_by_user_id(message.from_user.id)

        # Check stock data for the provided date
        result = self.check_stocks.check_stocks_get(auth_token=get_token, dateFrom=date_from)
        print(result)

        if result:
            for item in result:
                warehouse = item['warehouseName']
                quantity = item['quantity']
                in_way_to_client = item['inWayToClient']
                in_way_from_client = item['inWayFromClient']
                quantity_full = item['quantityFull']
                subject = item['subject']
                price = item['Price']
                discount = item['Discount']

                item_text = (
                    f"📦 Склад: {warehouse}\n"
                    f"📌 Наименование товара: {subject}\n"
                    f"📅 Количество: {quantity}\n"
                    f"🚚 В пути к клиенту: {in_way_to_client}\n"
                    f"🔄 В пути от клиента: {in_way_from_client}\n"
                    f"📊 Полное количество: {quantity_full}\n"
                    f"💵 Цена: {price}\n"
                    f"🎉 Скидка: {discount}%"
                )

                await message.answer(item_text, parse_mode="Markdown")
        else:
            await message.answer("Товары на указанную дату не найдены.")

        await message.answer(
            text="<b>Представлены все товары, которые доступны на выбранную дату</b>",
            parse_mode="HTML",
            reply_markup=await main_keyboard()
        )

        await state.clear()

