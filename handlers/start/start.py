import datetime
from keyboards.start_keyboards import autorizate_keyboard, main_keyboard
from aiogram import types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from text.start.start import start_message
from aiogram import Router
from state.token import AddToken


class StartHandler:
    def __init__(self, db, check_token):
        self.router = Router()
        self.db = db
        self.check_token = check_token
        self.router.callback_query(F.data == 'reset_token')(self.reset_token)
        self.router.message(AddToken.reset_token)(self.process_token)
        self.register_handlers()

    def register_handlers(self):
        self.router.message(CommandStart())(self.start)
        self.router.callback_query(F.data == 'autorizate')(self.autorizate)
        self.router.message(AddToken.token)(self.process_autorizate)

    async def start(self, message: types.Message, state: FSMContext):
        await message.answer(text=start_message, parse_mode="HTML")
        if self.db.user_exists(message.from_user.id):
            await message.answer(text="<b>Вы успешно авторизовались!</b>\n\n"
                                      "<i>Вам доступен весь фукнционал бота</i>",
                                 parse_mode="HTML",
                                 reply_markup=await main_keyboard()
                                 )
        else:
            await message.answer("<i>❗ Вам необходимо зарегистрироваться</i>",
                                 reply_markup=await autorizate_keyboard(),
                                 parse_mode="HTML")

    async def autorizate(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(text="Введите Ваш токен WB")
        await state.set_state(AddToken.token)

    async def process_autorizate(self, message: types.Message, state: FSMContext):
        await message.delete()
        response = self.check_token.update_commission(auth_token=message.text)

        if response.get('Status') == 'OK':
            self.db.add_user(message.from_user, message.text, datetime.datetime.now())
            await message.answer(
                text="Ваш токен успешно прошел проверку и привязан к вашего телеграмм аккаунту",
                parse_mode="HTML",
                reply_markup=await main_keyboard()
            )
            await state.clear()
        else:
            await message.answer(
                text="Ваш токен недействителен",
                parse_mode="HTML"
            )
            await state.clear()

    async def reset_token(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.message.edit_text(text="Введите новый токен")
        await state.set_state(AddToken.reset_token)

    async def process_token(self, message: types.Message, state: FSMContext):
        await message.delete()
        response = self.check_token.update_commission(auth_token=message.text)

        if response.get('Status') == 'OK':
            self.db.update_token(message.from_user.id, message.text, datetime.datetime.now())
            await message.answer(
                text="Ваш токен успешно прошел проверку и привязан к вашего телеграмм аккаунту",
                parse_mode="HTML",
                reply_markup=await main_keyboard()
            )
            await state.clear()
        else:
            await message.answer(
                text="Ваш токен недействителен",
                parse_mode="HTML"
            )
            await state.clear()
