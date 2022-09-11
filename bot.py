from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from middlewares import rate_limit
import datetime
from functions import *
from loader import *


# ----------------------------------- handlers  -----------------------------------
@rate_limit(limit=3)
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    if message.chat.type == 'private':
        if not DB.user_exists(message.from_user.id):
            try:
                await bot.send_sticker(message.from_user.id,
                                       sticker='CAACAgIAAxkBAAJJcmMY32AocCU6ZuniuNEQyDanJS27AAIBAQACVp29CiK-nw64wuY0KQQ')
            except:
                pass
            key = await Markup.welcom()
            mess = f'Меню'
            await bot.send_message(message.chat.id, mess, reply_markup=key)
    else:
        await message.answer('Писать боту можно только в личку')


@dp.callback_query_handler(text_contains='welcom', state='*')
async def welcom(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split(':')[-1]
    if call_data == 'order':
        key = await Markup.choice_thing()
        await call.message.edit_text(f'Создание заказа', reply_markup=None)
        await call.message.answer('Что вы хотите купить?', reply_markup=key)
        await orders.thing.set()
    elif call_data == 'connect':
        await call.message.edit_text(f'Для связи с менеджером...', reply_markup=None)
    else:
        await call.message.edit_reply_markup(None)
        mess = f'Здесь инфа о боте и про вас'
        await call.message.edit_text(mess, reply_markup=None)


@dp.message_handler(commands=['menu'], state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    key = await Markup.welcom()
    mess = f'Меню'
    await bot.send_message(message.chat.id, mess, reply_markup=key)


@rate_limit(limit=3)
@dp.message_handler(commands=['my_profile'], state='*')
async def my_profile(message: types.Message, state: FSMContext):
    await state.finish()
    if message.chat.type == 'private':
        user_id = message.from_user.id
        pass


# ----------------------------------- make order  -----------------------------------
class orders(StatesGroup):
    thing = State()
    brend = State()
    model = State()
    size = State()
    factors = State()
    telephone = State()
    confirm = State()


# создание заказа
@dp.message_handler(commands=['order'])
async def make_new_order(message: types.Message):
    if message.chat.type == 'private':
        key = await Markup.choice_thing()
        await message.answer('Что вы хотите купить?', reply_markup=key)
        await orders.thing.set()
    else:
        await message.answer('Писать боту можно только в личку')


# выбор вещи для покупки
@dp.callback_query_handler(text_contains='choice_thing', state=orders.thing)
async def make_new_order(call: types.CallbackQuery, state: FSMContext):
    thing_call = call.data.split(':')[-1]
    await state.update_data(thing=thing_call)
    if thing_call == 'shoes':
        await call.message.edit_text(f'🟢 Выбор обуви', reply_markup=None)
        key = shoesClass.choice_brend()
    elif thing_call == 'сlothes':
        await call.message.edit_text(f'🟢 Выбор одежды', reply_markup=None)
        key = clothesClass.choice_brend()
    else:
        await call.message.edit_text(f'🟢 Выбор аксессуара', reply_markup=None)
        key = accessoriesClass.choice_brend()

    await call.message.answer('Какой бренд вас интересует?', reply_markup=key)
    await orders.brend.set()


# выбор бренда
@dp.callback_query_handler(text_contains='choice_brend', state=orders.brend)
async def choice_brend(call: types.CallbackQuery, state: FSMContext):
    data_call = call.data.split(':')[-1]
    await state.update_data(brend=data_call)
    await call.message.edit_text(f'Вы выбрали {data_call}', reply_markup=None)
    thing = await state.get_data()
    if thing['thing'] == 'accessories':
        if data_call == 'Другое':
            await bot.send_message(call.from_user.id, 'Укажите свой бренд и уточняющие факторы для выбора модели '
                                                      '(цвет, стилистика или кастомизация)')
            await orders.factors.set()
        else:
            await bot.send_message(call.from_user.id, 'Уточняющие факторы для выбора модели '
                                                      '(цвет, стилистика или кастомизация)')
            await orders.factors.set()
    else:
        if data_call == 'Другое':
            await bot.send_message(call.from_user.id, 'Какой бренд и модель вас интересует? '
                                                      '\nЧтобы пропустить, напишите -')
            await orders.next()
        else:
            await bot.send_message(call.from_user.id, 'Какая модель вас интересует? '
                                                      '\nЧтобы пропустить, напишите -')
            await orders.next()


# выбор модели
@dp.message_handler(state=orders.model, content_types=['text'])
async def choice_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    thing = await state.get_data()
    if thing['thing'] == 'shoes':
        key = shoesClass.choice_size()
    elif thing['thing'] == 'сlothes':
        key = clothesClass.choice_size()
    else:
        key = accessoriesClass.choice_size()

    await bot.send_message(message.from_user.id, 'Какой размер вам необходим?', reply_markup=key)
    await orders.next()


# выбор размера
@dp.callback_query_handler(text_contains='choice_size', state=orders.size)
async def choice_size(call: types.CallbackQuery, state: FSMContext):
    data_call = call.data.split(':')[-1]
    await state.update_data(size=data_call)
    await call.message.edit_text(f'Вы выбрали {data_call}', reply_markup=None)
    await bot.send_message(call.from_user.id, 'Уточняющие факторы для выбора модели '
                                              '(цвет, стилистика или кастомизация)'
                                              '\nЧтобы пропустить, напишите -')
    await orders.next()


# уточняющие факторы
@dp.message_handler(state=orders.factors, content_types=['text'])
async def choice_factors(message: types.Message, state: FSMContext):
    await state.update_data(factors=message.text)
    await message.answer('Напишите номер телефона, чтобы мы смогли с вами связаться')
    await orders.next()


# телефон
@dp.message_handler(state=orders.telephone)
async def choice_telephone(message: types.Message, state: FSMContext):
    await state.update_data(telephone=message.text)
    key = await Markup.confirm_order()
    order_data = await state.get_data()

    if order_data['thing'] == 'accessories':
        message_order = f'Подтвердите ваш заказ:\n' \
                        f'Бренд: \n{order_data["brend"]}\n\n' \
                        f'Уточняющие факторы: \n{order_data["factors"]}\n\n' \
                        f'Телефон: \n{message.text}'
    else:
        message_order = f'Подтвердите ваш заказ:\n' \
                        f'Бренд: \n{order_data["brend"]}\n\n' \
                        f'Модель: \n{order_data["model"]}\n\n' \
                        f'Размер: \n{order_data["size"]}\n\n' \
                        f'Уточняющие факторы: \n{order_data["factors"]}\n\n' \
                        f'Телефон: \n{message.text}'

    await message.answer(message_order, reply_markup=key)
    await orders.next()


# подтверждение заказа
@dp.callback_query_handler(text_contains='confirm_order', state=orders.confirm)
async def confirm_order_to_finish(call: types.CallbackQuery, state: FSMContext):
    data_call = call.data.split(':')[-1]
    telegram_id = call.from_user.id
    username = call.from_user.first_name
    dt = datetime.datetime.now(tz=config.tz)
    order_data = await state.get_data()

    if data_call == 'yes':
        # добавление в базу данных

        if order_data['thing'] == 'accessories':
            message_order = f'Клиент: \n{username}\n\n' \
                            f'Бренд: \n{order_data["brend"]}\n\n' \
                            f'Уточняющие факторы: \n{order_data["factors"]}\n\n' \
                            f'Телефон: \n{order_data["telephone"]}'

            DB.new_row_user(telegram_id,
                                  username,
                                  dt,
                                  order_data['thing'],
                                  order_data["brend"],
                                  '-',
                                  '-',
                                  order_data["factors"],
                                  order_data["telephone"])
        else:
            message_order = f'Клиент: \n{username}\n\n' \
                            f'Вещь: \n{order_data["thing"]}\n\n' \
                            f'Бренд: \n{order_data["brend"]}\n\n' \
                            f'Модель: \n{order_data["model"]}\n\n' \
                            f'Размер: \n{order_data["size"]}\n\n' \
                            f'Уточняющие факторы: \n{order_data["factors"]}\n\n' \
                            f'Телефон: \n{order_data["telephone"]}'
            DB.new_row_user(telegram_id,
                                  username,
                                  dt,
                                  order_data['thing'],
                                  order_data["brend"],
                                  order_data["model"],
                                  order_data["size"],
                                  order_data["factors"],
                                  order_data["telephone"])

        await bot.send_message(config.ORDER_CHAT_ID, message_order)
        await call.message.edit_text(f'🟢 Ваш заказ отправлен', reply_markup=None)
        await state.finish()

    elif data_call == 'stop':
        await call.message.edit_text('Вы отменили отправку заказа', reply_markup=None)
        await state.finish()


# ----------------------------------- admin's handlers  -----------------------------------
@dp.message_handler(commands=['chat_info'])
async def chat_info(message: types.Message):
    if await admins_test(message):
        await bot.send_message(message.chat.id, message.chat.id)


@dp.message_handler(commands=['dump'])
async def dump(message: types.Message):
    if await admins_test(message):
        await make_dump()


@dp.message_handler(commands=['exel'])
async def exel(message: types.Message):
    if await admins_test(message):
        DB.make_xlsx()
        with open('KIFY_bot.xlsx', "rb") as f:
            await bot.send_document(config.EXEL, f)


@dp.message_handler(commands=['restart_data'])
async def restart_data(message: types.Message):
    if await admins_test(message):
        try:
            DB.close()
            DB.connect()
            await bot.send_message(config.admin_id, 'Перезагрузка завершена')
        except:
            await bot.send_message(config.admin_id, 'Ошибка перезагрузки')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=start_bot, on_shutdown=stop_bot, skip_updates=False)
