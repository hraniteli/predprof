from config import TOKEN
import csv
import datetime
from providers import check_user_exist, check_user_admin, check_akes, add_user_in_db, del_user_from_akes, get_data
import re
import service
import telebot
from telebot import types


bot = telebot.TeleBot(TOKEN)


def check_admin(func):
    def wrapper(message):
        check = check_user_admin(message.chat.id)
        if check == 'Пользователь не найден.':
            bot.send_message(message.chat.id,
                             'Вы не зарегистрированы. Обратитесь к администратору, чтобы она вас зарегестрировал.')
            return 0
        if check:
            func(message)
        else:
            bot.send_message(message.chat.id, 'У вас недостаточно прав.')

    return wrapper


def check_user(func):
    def wrapper(message):
        check = check_user_exist(message.chat.id)
        if check == 'Пользователь не найден.':
            bot.send_message(message.chat.id,
                             'Вы не зарегистрированы. Обратитесь к администратору, чтобы она вас зарегестрировал.')
            return 0
        if check:
            func(message)

    return wrapper


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Здравствуйте. Это бот для мониторинг комплекса энергосбережения.")


@bot.message_handler(commands=['xls'])
@check_user
def get_xls(message):
    msg = bot.send_message(message.chat.id, 'Введите серийный номер АКЭС.')
    bot.register_next_step_handler(msg, get_xls_by_sn)


def get_xls_by_sn(message):
    if len(re.findall('\D', message.text.strip())) > 0:
        bot.send_message(message.chat.id, 'Недопустимый формат серийного номера.')
        return 0
    sn = int(message.text.strip())
    data = get_data(sn, message)
    if data == 'Нет АКЭС':
        bot.send_message(message.chat.id, 'АКЭС не существует.')
        return 0
    if data == 'Нет доступа':
        bot.send_message(message.chat.id, 'У вас не досткпа к этому АКЭС.')
        return 0
    xls_name = service.get_xls(data)
    with open(f'tmp/xls/{xls_name}.csv', 'r') as fd:
        bot.send_document(message.chat.id, fd)


@bot.message_handler(commands=['grphc'])
@check_user
def get_grphc(message):
    msg = bot.send_message(message.chat.id, 'Введите серийный номер АКЭС.')
    bot.register_next_step_handler(msg, grphc_period)


def grphc_period(message):
    if len(re.findall('\D', message.text.strip())) > 0:
        bot.send_message(message.chat.id, 'Недопустимый формат серийного номера.')
        return 0
    sn = int(message.text.strip())
    if not check_akes(sn):
        bot.send_message(message.chat.id, 'АКЭС не существует.')
        return 0
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='За этот день', callback_data=f'get_grphc_day {sn}'))
    keyboard.add(types.InlineKeyboardButton(text='За неделю', callback_data=f'get_grphc_week {sn}'))
    bot.send_message(message.chat.id, 'За какой период?', reply_markup=keyboard)


@bot.message_handler(commands=['add_user'])
@check_admin
def add_user(message):
    if check_admin(message.chat.id):
        msg = bot.send_message(message.chat.id, 'Укажите uid.')
        bot.register_next_step_handler(msg, add_user_handler)


def add_user_handler(message):
    if len(re.findall('\D+', message.text.strip())) != 0:
        bot.send_message(message.chat.id, 'Недопустимый формат uid.')
        return 0
    uid = message.text.strip()
    user = add_user_in_db(uid)
    if user == 0:
        bot.send_message(message.chat.id, 'Такой пользователь уже есть.')
    else:
        bot.send_message(message.chat.id, 'Готово!')


@bot.message_handler(commands=['add_akes'])
@check_admin
def add_akes(message):
    msg = bot.send_message(message.chat.id,
                           'Введите uid пользователя и серийный номер АКЭС, к которому надо выдать доступ.')
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
        bot.send_message(message.chat.id, 'Недопустимый формат uid или серийного номера.')
        return 0
    uid, sn = re.findall('\d+', message.text)
    akes = add_user_to_akes(uid, int(sn))
    if akes == 0:
        bot.send_message(message.chat.id, 'У пользователя уже есть достуа к этой АКЭС.')
        return 0
    if akes == -1:
        bot.send_message(message.chat.id, 'АКЭС не существует.')
        return 0
    bot.send_message(message.chat.id, 'АКЭС добавлена.')


@bot.message_handler(commands=['del_akes'])
@check_admin
def del_akes(message):
    msg = bot.send_message(message.chat.id,
                           'Введите uid пользователя и серийный номер АКЭС, к которому надо запретить доступ.')
    bot.register_next_step_handler(msg, del_akes_handler)


def del_akes_handler(message):
    check = True
    mes = re.findall('\S+', message.text)
    if len(mes) != 2:
        check = False
    for x in [re.findall('\D+', x) for x in mes]:
        if len(x) > 0:
            check = False
            break
    if not check:
        bot.send_message(message.chat.id, 'Недопустимый формат uid или серийного номера.')
        return 0
    uid, sn = re.findall('\d+', message.text)
    akes = del_user_from_akes(uid, int(sn))
    if akes == 0:
        bot.send_message(message.chat.id, 'У пользователя и так нет достуа к этой АКЭС.')
        return 0
    if akes == -1:
        bot.send_message(message.chat.id, 'АКЭС не существует.')
        return 0
    bot.send_message(message.chat.id, 'АКЭС удалена.')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    call_data, sn = call.data.split(' ')
    sn = int(sn)
    message = call.message
    if call_data == 'get_grphc_day':
        data = get_data(sn, message, 'day')
        if data == 'Нет доступа':
            bot.send_message(message.chat.id, 'У вас не досткпа к этому АКЭС.')
            return 0
        answer = service.get_grphc(data)
    if call_data == 'get_grphc_week':
        data = get_data(sn, message, 'week')
        if data == 'Нет доступа':
            bot.send_message(message.chat.id, 'У вас не досткпа к этому АКЭС.')
            return 0
        answer = service.get_grphc(data)
    bot.send_photo(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling()
