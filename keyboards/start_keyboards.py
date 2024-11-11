from aiogram import types


async def autorizate_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="ПРИВЯЗАТЬ ТОКЕН",
                    callback_data="autorizate"
                )
            ]]
    )


async def main_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="🏪 Статистика",
                    callback_data="state"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="⌛️ Контроль остатков по городам",
                    callback_data="control_tovar"
                ),
            ],
            # [
            #     types.InlineKeyboardButton(
            #         text="🚗 Отслеживание заказов",
            #         callback_data="watch_order"
            #     ),
            # ],
            [
                types.InlineKeyboardButton(
                    text="🏆 Коэфиценты складов",
                    callback_data="control"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="🪃 Поменять токен",
                    callback_data="reset_token"
                ),
            ],
        ]
    )


async def time_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="На сегодня",
                    callback_data="today"
                ),
                types.InlineKeyboardButton(
                    text="За вчера",
                    callback_data="yesterday"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Введу сам",
                    callback_data="self_go"
                ),
            ]
        ]
    )


async def state_keyboard_select_1():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Статистика по продажам",
                    callback_data="sale_state"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Статистика по заказам",
                    callback_data="order_stare"
                ),
            ],
        ]
    )


async def coef_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Получить коэфиценты по всем складам",
                    callback_data="all_coef"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Получить коэфицент для определенного склада",
                    callback_data="one_coef"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Бесплатная поставка",
                    callback_data="coef"
                ),
            ]
        ]
    )


async def name_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Казань",
                    callback_data="117986"
                ),
                types.InlineKeyboardButton(
                    text="Коледино",
                    callback_data="507"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Электросталь",
                    callback_data="120762"
                ),
                types.InlineKeyboardButton(
                    text="Тула",
                    callback_data="206348"
                ),
            ]
        ]
    )

async def name_keyboard_free():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Казань",
                    callback_data="117986_free"
                ),
                types.InlineKeyboardButton(
                    text="Коледино",
                    callback_data="507_free"
                ),
            ],
            [
                types.InlineKeyboardButton(
                    text="Электросталь",
                    callback_data="120762_free"
                ),
                types.InlineKeyboardButton(
                    text="Тула",
                    callback_data="206348_free"
                ),
            ]
        ]
    )