from aiogram import Bot, types
from aiogram.utils.callback_data import CallbackData
import config


class Shoes:
    def __init__(self):
        self.list_brends = ['Nike (Jordan)',
                            'Adidas (Y-3)',
                            'New balance',
                            'Yeezy',
                            'Asics',
                            'Converse',
                            'Timberland',
                            'Premiata',
                            'Другое']
        self.list_size = ['40 | 7 | 25 муж.',
                          '40,5 | 7,5 | 25,5 муж.',
                          '41 | 8 | 26 муж.',
                          '42 | 8,5 | 26,5 муж.',
                          '42,5 | 9 | 27 муж.',
                          '43 | 9,5 | 27,5 муж.',
                          '44 | 10 | 28 муж.',
                          '44,5 | 10,5 | 28,5 муж.',
                          '45 | 11 | 29 муж.',
                          '45,5 | 11,5 | 29,5 муж.',
                          '46 | 12 | 30 муж.',
                          '46,5 | 12,5 | 30,5 муж.',
                          '47,5 | 13 | 31 муж.',
                          '48 | 13,5 | 31,5 муж.',
                          '35, 5 | 5 | 22 жен.',
                          '36 | 5, 5 | 22, 5 жен.',
                          '36, 5 | 6 | 23 жен.',
                          '37, 5 | 6, 5 | 23, 5 жен.',
                          '38 | 7 | 24 жен.',
                          '38, 5 | 7, 5 | 24, 5 жен.',
                          '39 | 8 | 25 жен.',
                          '40 | 8, 5 | 25, 5 жен.',
                          '40, 5 | 9 | 26 жен.',
                          '41 | 9, 5 | 26, 5 жен.',
                          '42 | 10 | 27 жен.',
                          '35, 5 | 3, 5Y | 22, 5, дет.',
                          '36 | 4Y | 23, дет.',
                          '36, 5 | 4, 5Y | 23, 5, дет.',
                          '37, 5 | 5Y | 23, 5, дет.',
                          '38 | 5, 5Y | 24, дет.',
                          '38, 5 | 6Y | 24, дет.',
                          '39 | 6, 5Y | 24, 5, дет.',
                          '40 | 7Y | 25, дет.',
                          ]

    def choice_brend(self):
        data = CallbackData('choice_brend', 'action')
        keyboard = types.InlineKeyboardMarkup(row_width=3)

        list_brends_btn = []
        for i in self.list_brends:
            btn = types.InlineKeyboardButton(text=i, callback_data=data.new(action=i))
            list_brends_btn.append(btn)

        keyboard.add(*list_brends_btn)
        return keyboard

    def choice_size(self):
        data = CallbackData('choice_size', 'action')
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        list_size_btn = []
        for i in self.list_size:
            btn = types.InlineKeyboardButton(text=i, callback_data=data.new(action=i))
            list_size_btn.append(btn)

        keyboard.add(*list_size_btn)
        return keyboard


class Сlothes:
    def __init__(self):
        self.list_brends = ['Nike (Jordan)',
                            'Adidas (Y-3)',
                            'New balance',
                            'Reebok',
                            'Puma',
                            'TheNorthFace',
                            'Supreme',
                            'Alpha Industries',
                            'Timberland',
                            'Levis',
                            'UniQlo',
                            'Polo Ralph Lauren',
                            'Tommy Hilfiger',
                            'Guess',
                            'Charhartt',
                            'Stussy',
                            'Lacoste',
                            'Balenciaga',
                            'Другое']
        self.list_size = ['S муж.',
                          'M муж.',
                          'L муж.',
                          'XL муж.',
                          'XS жен.',
                          'S жен.',
                          'M жен.',
                          'L жен.',
                          'XL жен.',
                          'Ваш вариант']

    def choice_brend(self):
        data = CallbackData('choice_brend', 'action')
        keyboard = types.InlineKeyboardMarkup(row_width=3)

        list_brends_btn = []
        for i in self.list_brends:
            btn = types.InlineKeyboardButton(text=i, callback_data=data.new(action=i))
            list_brends_btn.append(btn)

        keyboard.add(*list_brends_btn)
        return keyboard

    def choice_size(self):
        data = CallbackData('choice_size', 'action')
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        list_size_btn = []
        for i in self.list_size:
            btn = types.InlineKeyboardButton(text=i, callback_data=data.new(action=i))
            list_size_btn.append(btn)

        keyboard.add(*list_size_btn)
        return keyboard


class Аccessories:
    def __init__(self):
        self.list_brends = ['Nike (Jordan)',
                            'Adidas (Y-3)',
                            'New balance',
                            'Reebok',
                            'Puma',
                            'TheNorthFace',
                            'Supreme',
                            'Burberry',
                            'Levis',
                            'Medicom Toy',
                            'Guess',
                            'Alux',
                            'Louis Vuitton',
                            'Guess',
                            'Charhartt',
                            'Stussy',
                            'Lacoste',
                            'Balenciaga',
                            'Casio',
                            'Другое']

    def choice_brend(self):
        data = CallbackData('choice_brend', 'action')
        keyboard = types.InlineKeyboardMarkup(row_width=3)

        list_brends_btn = []
        for i in self.list_brends:
            btn = types.InlineKeyboardButton(text=i, callback_data=data.new(action=i))
            list_brends_btn.append(btn)

        keyboard.add(*list_brends_btn)
        return keyboard


async def confirm_order():
    data = CallbackData('confirm_order', 'action')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_confirm = types.InlineKeyboardButton(text='Подтвердить',
                                             callback_data=data.new(action='yes'))
    btn_stop = types.InlineKeyboardButton(text='Отменить отправку заказа',
                                          callback_data=data.new(action='stop'))
    keyboard.add(btn_confirm, btn_stop)
    return keyboard


async def choice_thing():
    data = CallbackData('choice_thing', 'action')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_Shoes = types.InlineKeyboardButton(text='Обувь',
                                           callback_data=data.new(action='shoes'))
    btn_Сlothes = types.InlineKeyboardButton(text='Одежда',
                                             callback_data=data.new(action='сlothes'))
    btn_Аccessories = types.InlineKeyboardButton(text='Аксессуары',
                                                 callback_data=data.new(action='accessories'))
    keyboard.add(btn_Shoes, btn_Сlothes, btn_Аccessories)
    return keyboard


async def welcom():
    data = CallbackData('welcom', 'action')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_1 = types.InlineKeyboardButton(text='Сделать заказ',
                                       callback_data=data.new(action='order'))
    btn_2 = types.InlineKeyboardButton(text='Cвязь с менеджером',
                                       callback_data=data.new(action='connect'))
    btn_3 = types.InlineKeyboardButton(text='Информация',
                                       callback_data=data.new(action='info'))

    keyboard.add(btn_1, btn_2, btn_3)
    return keyboard