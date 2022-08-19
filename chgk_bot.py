import telebot
from telebot import types
from time import asctime
import chgk_api
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


bot = telebot.TeleBot('5420233585:AAFUeq6tn5a-DG3FkgqYEYEUF6aqR-MDoTM')


id_dct = {}


@bot.message_handler(commands=['start'])
def start(m):
    global id_dct
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вопрос ЧГК")
    markup.add(item1)
    user_id = m.from_user.id
    id_dct[user_id] = [[], ['', '']]
    bot.send_message(m.chat.id, 'Нажмите: \nВопрос ЧГК для получения вопроса',
                     reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        soup = chgk_api.get_soup()
        all_text = chgk_api.get_all_text(soup)
        outp_message = ''
        question = ''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        global id_dct
        user_id = message.from_user.id
        try:
            id_dct[user_id][0].append(message.text.strip().lower())
            if message.text.strip().lower() == 'вопрос чгк':
                item2 = types.KeyboardButton("Ответ")
                markup.add(item2)
                if id_dct[user_id][0] == ['вопрос чгк']:
                    question = chgk_api.get_question(all_text, soup)
                    id_dct[user_id][1][0] = chgk_api.get_answer(all_text)
                    id_dct[user_id][1][1] = chgk_api.get_comment(all_text)
                    outp_message = question
                    bot.send_message(message.chat.id, outp_message,
                                     reply_markup=markup)
                else:
                    del id_dct[user_id][0][0]
                bot.send_message(message.chat.id, 'Напишите ответ или' +
                                 ' Нажмите "Ответ", чтобы '
                                 + 'получить ответ')
            elif message.text.strip().lower() == 'ответ':
                item1 = types.KeyboardButton("Вопрос ЧГК")
                markup.add(item1)
                if id_dct[user_id][0] == ['вопрос чгк', 'ответ']:
                    outp_message = ('Ответ: ' + id_dct[user_id][1][0] + '\n\n'
                                    + id_dct[user_id][1][1])
                else:
                    outp_message = 'Вы не запросили вопрос!'
                id_dct[user_id][0].clear()
                bot.send_message(message.chat.id, outp_message,
                                 reply_markup=markup)
            elif similar(id_dct[user_id][1][0].lower(),
                         message.text.strip().lower()) >= 0.7:
                item1 = types.KeyboardButton("Вопрос ЧГК")
                markup.add(item1)
                id_dct[user_id][0].clear()
                bot.send_message(message.chat.id, 'Абсолютно верно!' + '\n\n' +
                                 id_dct[user_id][1][1],
                                 reply_markup=markup)
            else:
                if id_dct[user_id][0][0] == 'вопрос чгк':
                    bot.send_message(message.chat.id, 'Ответ неверный :(\n')
                else:
                    bot.send_message(message.chat.id, 'Вы ввели незнакомую \
                        команду'
                                     + '\nНажмите "Вопрос ЧГК" для получения '
                                     + 'вопроса')
                del id_dct[user_id][0][-1]
        except KeyError:
            bot.send_message(message.chat.id, 'Введите комманду /start')
    except ConnectionError:
        with open('log.txt', 'a') as output_f:
            output_f.write(asctime() + ': ' + 'ConnectionError\n')


bot.polling(none_stop=True, interval=0)
