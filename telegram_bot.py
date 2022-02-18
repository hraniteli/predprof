import telebot
from telebot import types
import service
import datetime
from providers import get_data, add_user_in_db, add_user_to_akes
import re

TOKEN = '5283098146:AAH3C8OszNaXw3jJL7TjSPF8Zty2fq2PTRg'
bot = telebot.TeleBot(TOKEN)
res_data = [[datetime.datetime(2022, 2, 16, 14, 0, 2), datetime.datetime(2022, 2, 16, 14, 6, 13), 0.997, 0.999, 0.999,
             89400.0, 84300.0, 81600.0, 230.0, 231.0, 227.0, 7.51, '800000005773'],
            [datetime.datetime(2022, 2, 16, 19, 7, 22), datetime.datetime(2022, 2, 16, 19, 7, 22), -0.999, 0.999,
             -0.975, 17100.0, 17400.0, 20400.0, 231.0, 229.0, 230.0, None, '800000005773'],
            [datetime.datetime(2022, 2, 16, 20, 7, 34), datetime.datetime(2022, 2, 16, 20, 7, 34), 0.999, -0.994,
             -0.993, 8400.0, 9000.0, 12000.0, 231.0, 231.0, 230.0, None, '800000005773'],
            [datetime.datetime(2022, 2, 16, 18, 15, 30), datetime.datetime(2022, 2, 16, 20, 21, 30), -0.966, -0.968,
             -0.965, 18486.0, 16380.0, 13530.0, 224.42, 224.07, 224.42, 21.97, '800000005773']]


@bot.message_handler(commands=['xls'])
def get_xls(message):
    with open('tmp/example.csv', 'rb') as fd:
        bot.send_document(message.chat.id, fd)


@bot.message_handler(commands=['grphc'])
def get_grphc(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='За этот день', callback_data='get_grphc_day'))
    keyboard.add(types.InlineKeyboardButton(text='За неделю', callback_data='get_grphc_week'))
    bot.send_message(message.chat.id, 'За какой период?', reply_markup=keyboard)


@bot.message_handler(commands=['add_user'])
def add_user(message):
    if service.check_admin(message.chat.id):
        msg = bot.send_message(message.chat.id, 'Укажите uid')
        bot.register_next_step_handler(msg, add_user_handler)


def add_user_handler(message):
    if len(re.findall('\D+', message.text.strip())) != 0:
        bot.send_message(message.chat.id, 'Недопустимый формат uid')
        return 0
    uid = message.text.strip()
    user = add_user_in_db(uid)
    if user == 0:
        bot.send_message(message.chat.id, 'Такой пользователь уже есть')
    else:
        bot.send_message(message.chat.id, 'Готово')


@bot.message_handler(commands=['add_akes'])
def add_akes(message):
    msg = bot.send_message(message.chat.id,
                           'Введите uid пользователя и серийный номер АКЭС, к которому надо выдать доступ')
    bot.register_next_step_handler(msg, add_akes_handler)


def add_akes_handler(message):
    check = True
    mes = re.findall('\S+', message.text)
    if len(mes) != 2:
        check = False
    for x in [re.findall('\D+', x) for x in mes]:
        if len(x) > 0:
            check = False
            break
    if not check:
        bot.send_message(message.chat.id, 'Недопустимый формат uid или серийного номера')
        return 0
    uid, sn = re.findall('\d+', message.text)
    akes = add_user_to_akes(uid, sn)
    if akes == 0:
        bot.send_message(message.chat.id, 'У пользователя уже есть достуа к этой АКЭС')
    if akes == -1:
        bot.send_message(message.chat.id, 'АКЭС не существует')
    else:
        bot.send_message(message.chat.id, 'АКЭС добавлена')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'get_grphc_day':
        data = get_data('day')
        answer = service.get_grphc(data)
    if call.data == 'get_grphc_week':
        data = get_data('week')
        answer = service.get_grphc(data)
    bot.send_photo(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling()
