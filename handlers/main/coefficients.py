import datetime
import re
import tempfile

import pandas as pd
from aiogram.types import FSInputFile

from keyboards.start_keyboards import main_keyboard, time_keyboard, coef_keyboard, name_keyboard, name_keyboard_free
from aiogram import types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from state.date_state import DateState
from text.start.start import start_message
from aiogram import Router
from state.token import AddToken


class CoefficientsHandler:
    def __init__(self, db, check_coef):
        self.router = Router()
        self.db = db
        self.check_coef = check_coef
        self.register_handlers()

    def register_handlers(self):
        self.router.callback_query(F.data == 'control')(self.control)
        self.router.callback_query(F.data == 'all_coef')(self.all_coef)
        self.router.callback_query(F.data == 'one_coef')(self.one_coef)
        self.router.callback_query(F.data == 'coef')(self.coef)
        self.router.callback_query(F.data.in_(['117986', '507', '120762', '206348']))(self.handle_warehouse)
        self.router.callback_query(F.data.in_(['117986_free', '507_free', '120762_free', '206348_free']))(self.handle_warehouse_free)

    async def control(self, callback: types.CallbackQuery):
        await callback.message.answer(text="📍 Коэфиценты складов", reply_markup=await coef_keyboard())

    async def all_coef(self, callback: types.CallbackQuery):
        result = self.check_coef.check_coef(self.db.get_token_by_user_id(callback.from_user.id))
        if result:
            df = pd.DataFrame(result)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                excel_file_path = temp_file.name
                df.to_excel(excel_file_path, index=False)

            await callback.message.answer_document(FSInputFile(excel_file_path),
                                                   caption="💾 Коэфиценты всех складов",
                                                   reply_markup=await main_keyboard())
        else:
            await callback.message.answer("❌ Данные по продажам не найдены на указанную дату.")

    async def one_coef(self, callback: types.CallbackQuery):
        await callback.message.edit_text("Выбери для какого склада получить коэфицент",
                                         reply_markup=await name_keyboard())

    async def handle_warehouse(self, callback: types.CallbackQuery):
        warehouse_id = callback.data

        warehouse_names = {
            '117986': 'Казань',
            '507': 'Коледино',
            '120762': 'Электросталь',
            '206348': 'Тула'
        }
        warehouse_name = warehouse_names.get(warehouse_id, "Склад")

        result = self.check_coef.check_coef(
            auth_token=self.db.get_token_by_user_id(callback.from_user.id),
            warehouseIDs=warehouse_id
        )

        if result:
            formatted_entries = []
            for entry in result:
                if entry['coefficient'] == -1:
                    coefficient_text = "Поставка недоступна"
                elif entry['coefficient'] == 0:
                    coefficient_text = "Поставка бесплатна"
                else:
                    coefficient_text = f"{entry['coefficient']}"

                formatted_entries.append(
                    f"📅 Дата: {entry['date'][:10]}\n"
                    f"🏢 Склад: {entry['warehouseName']} (ID: {entry['warehouseID']})\n"
                    f"📦 Тип бокса: {entry['boxTypeName']}\n"
                    f"📊 Коэффициент: {coefficient_text}\n"
                )

            def split_into_chunks(entries, max_length=4096):
                current_chunk = ""
                for entry in entries:
                    if len(current_chunk) + len(entry) > max_length:
                        yield current_chunk
                        current_chunk = entry
                    else:
                        current_chunk += entry + "\n\n"
                if current_chunk:
                    yield current_chunk

            await callback.message.answer(f"Результаты для склада {warehouse_name}:")
            for chunk in split_into_chunks(formatted_entries):
                await callback.message.answer(chunk)

        else:
            # Message if no data is found for the selected warehouse
            await callback.message.answer(f"Нет данных для склада {warehouse_name}.")

    async def coef(self, callback: types.CallbackQuery):
        await callback.message.edit_text("Выбери для какого склада проверить на бесплатный коэфицент",
                                         reply_markup=await name_keyboard_free())

    async def handle_warehouse_free(self, callback: types.CallbackQuery):
        warehouse_id = callback.data.replace('_free', '')

        # Mapping warehouse IDs to their names for better readability
        warehouse_names = {
            '117986': 'Казань',
            '507': 'Коледино',
            '120762': 'Электросталь',
            '206348': 'Тула'
        }
        warehouse_name = warehouse_names.get(warehouse_id, "Склад")

        result = self.check_coef.check_coef(
            auth_token=self.db.get_token_by_user_id(callback.from_user.id),
            warehouseIDs=warehouse_id
        )

        # Filter entries with a coefficient of 0 (free delivery)
        free_delivery_entries = [entry for entry in result if entry['coefficient'] == 0]

        if free_delivery_entries:
            formatted_entries = [
                f"📅 Дата: {entry['date'][:10]}\n"
                f"🏢 Склад: {entry['warehouseName']} (ID: {entry['warehouseID']})\n"
                f"📦 Тип бокса: {entry['boxTypeName']}\n"
                f"📊 Коэффициент: Поставка бесплатна\n"
                for entry in free_delivery_entries
            ]

            # Function to split the message into chunks within the Telegram message length limit
            def split_into_chunks(entries, max_length=4096):
                current_chunk = ""
                for entry in entries:
                    if len(current_chunk) + len(entry) > max_length:
                        yield current_chunk
                        current_chunk = entry
                    else:
                        current_chunk += entry + "\n\n"
                if current_chunk:
                    yield current_chunk

            # Send each chunk of the formatted message
            await callback.message.answer(f"Результаты для склада {warehouse_name} с бесплатной доставкой:")
            for chunk in split_into_chunks(formatted_entries):
                await callback.message.answer(chunk)

        else:
            # Message if no free delivery data is found for the selected warehouse
            await callback.message.answer(f"Нет бесплатной доставки для склада {warehouse_name}.")
