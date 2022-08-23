import telebot
from telebot import types
from time import asctime
import chgk_parser
from difflib import SequenceMatcher
import os


TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(token=TOKEN)


info_dct = {}


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


@bot.message_handler(commands=['start'])
def start(m):
    global info_dct
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вопрос ЧГК")
    markup.add(item1)
    chat_id = m.chat.id
    info_dct[chat_id] = [[], ['', '']]
    bot.send_message(m.chat.id, 'Нажмите: \nВопрос ЧГК для получения вопроса',
                     reply_markup=markup)


@bot.message_handler(commands=['del_markup'])
def delete_markup(message):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Клавиатура удалена, чтобы снова \
воспользоваться ботом введите команду /start', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        soup = chgk_parser.get_soup()
        all_text = chgk_parser.get_all_text(soup)
        outp_message = ''
        question = ''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        global info_dct
        chat_id = message.chat.id
        try:
            info_dct[chat_id][0].append(message.text.strip().lower())
            if message.text.strip().lower() == 'вопрос чгк':
                item2 = types.KeyboardButton("Ответ")
                markup.add(item2)
                if info_dct[chat_id][0] == ['вопрос чгк']:
                    question = chgk_parser.get_question(all_text, soup)
                    info_dct[chat_id][1][0] = chgk_parser.get_answer(all_text)
                    info_dct[chat_id][1][1] = chgk_parser.get_comment(all_text)
                    outp_message = question
                    bot.send_message(message.chat.id, outp_message,
                                     reply_markup=markup)
                else:
                    del info_dct[chat_id][0][0]
                bot.send_message(message.chat.id, 'Напишите ответ или' +
                                 ' Нажмите "Ответ", чтобы '
                                 + 'получить ответ')
            elif message.text.strip().lower() == 'ответ':
                item1 = types.KeyboardButton("Вопрос ЧГК")
                markup.add(item1)
                if info_dct[chat_id][0] == ['вопрос чгк', 'ответ']:
                    outp_message = ('Ответ: ' + info_dct[chat_id][1][0] +
                                    '\n\n' + info_dct[chat_id][1][1])
                else:
                    outp_message = 'Вы не запросили вопрос!'
                info_dct[chat_id][0].clear()
                bot.send_message(message.chat.id, outp_message,
                                 reply_markup=markup)
            elif similar(info_dct[chat_id][1][0].lower(),
                         message.text.strip().lower()) >= 0.7:
                item1 = types.KeyboardButton("Вопрос ЧГК")
                markup.add(item1)
                info_dct[chat_id][0].clear()
                bot.send_message(message.chat.id, 'Абсолютно верно!' + '\n\n' +
                                 info_dct[chat_id][1][1],
                                 reply_markup=markup)
            else:
                if info_dct[chat_id][0][0] == 'вопрос чгк':
                    bot.send_message(message.chat.id, 'Ответ неверный :(\n')
                else:
                    bot.send_message(message.chat.id,
                                     'Вы ввели незнакомую команду \
                                    \nНажмите "Вопрос ЧГК" для получения '
                                     + 'вопроса')
                del info_dct[chat_id][0][-1]
        except KeyError:
            bot.send_message(message.chat.id, 'Введите комманду /start')
    except ConnectionError:
        print(asctime() + ': ' + 'ConnectionError\n')


bot.polling(none_stop=True, interval=0)
