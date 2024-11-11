import datetime
import re
import tempfile

import pandas as pd
from aiogram.types import FSInputFile

from keyboards.start_keyboards import state_keyboard_select_1, main_keyboard
from aiogram import types, F, Bot
from aiogram.fsm.context import FSMContext

from state.StateList import StateState
from aiogram import Router


class StateHandler:
    def __init__(self, db, check_incomes):
        self.router = Router()
        self.db = db
        self.check_incomes = check_incomes
        self.register_handlers()

    def register_handlers(self):
        self.router.callback_query(F.data == 'sale_state')(self.sale_state)
        self.router.callback_query(F.data == 'order_stare')(self.order_stare)
        self.router.callback_query(F.data == 'state')(self.state_sale)
        self.router.message(StateState.sale_state)(self.procces_generate_sale)
        self.router.message(StateState.order_state)(self.procces_generate_order)

    @staticmethod
    async def state_sale(callback: types.CallbackQuery):
        await callback.message.edit_text(text="Выберите какой отчет нужно сформировать",
                                         reply_markup=await state_keyboard_select_1())

    @staticmethod
    async def sale_state(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(text="Напишите дату для которой нужно сформировать отчет по продажам")
        await state.set_state(StateState.sale_state)

    @staticmethod
    async def order_stare(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(text="Напишите дату для которой нужно сформировать отчет по заказам")
        await state.set_state(StateState.order_state)

    async def procces_generate_sale(self, msg: types.Message):
        date_text = msg.text
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_text):
            await msg.answer("❌ Пожалуйста, введите дату в формате YYYY-MM-DD.")
            return

        try:
            date_from = datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            await msg.answer("❌ Неверный формат даты. Попробуйте снова.")
            return

        get_token = self.db.get_token_by_user_id(msg.from_user.id)

        result = self.check_incomes.check_sales(auth_token=get_token, dateFrom=date_from)

        if result:
            df = pd.DataFrame(result)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                excel_file_path = temp_file.name
                df.to_excel(excel_file_path, index=False)

            await msg.answer_document(FSInputFile(excel_file_path),
                                      caption="💾 Ваши данные по продажам в формате Excel",
                                      reply_markup=await main_keyboard())
        else:
            await msg.answer("❌ Данные по продажам не найдены на указанную дату.")

    async def procces_generate_order(self, msg: types.Message):
        date_text = msg.text
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_text):
            await msg.answer("❌ Пожалуйста, введите дату в формате YYYY-MM-DD.")
            return

        try:
            date_from = datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            await msg.answer("❌ Неверный формат даты. Попробуйте снова.")
            return

        get_token = self.db.get_token_by_user_id(msg.from_user.id)

        result = self.check_incomes.check_order(auth_token=get_token, dateFrom=date_from)

        if result:
            df = pd.DataFrame(result)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                excel_file_path = temp_file.name
                df.to_excel(excel_file_path, index=False)

            await msg.answer_document(FSInputFile(excel_file_path),
                                      caption="💾 Ваши данные по заказам в формате Excel",
                                      reply_markup=await main_keyboard())
        else:
            await msg.answer("❌ Данные по продажам не найдены на указанную дату")
