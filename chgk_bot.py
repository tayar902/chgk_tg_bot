import telebot
from telebot import types
from time import asctime
import chgk_api

bot = telebot.TeleBot('5420233585:AAFUeq6tn5a-DG3FkgqYEYEUF6aqR-MDoTM')


@bot.message_handler(commands=['start'])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вопрос ЧГК")
    markup.add(item1)
    bot.send_message(m.chat.id, 'Нажми: \nВопрос ЧГК для получения вопроса',
                     reply_markup=markup)


outp = ''


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        all_text = chgk_api.get_all_text()
        answer = ''
        question = ''
        global outp
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if message.text.strip() == 'Вопрос ЧГК':
            question = chgk_api.get_question(all_text)
            outp = ''
            outp = chgk_api.get_answer(all_text)
            answer = question
            item2 = types.KeyboardButton("Ответ")
            markup.add(item2)
            bot.send_message(message.chat.id, answer, reply_markup=markup)
        elif message.text.strip() == 'Ответ':
            item1 = types.KeyboardButton("Вопрос ЧГК")
            markup.add(item1)
            if outp != '':
                answer = outp
            else:
                answer = 'Вы не запросили вопрос!'
            bot.send_message(message.chat.id, answer, reply_markup=markup)
    except ConnectionError:
        with open('log.txt', 'a') as output_f:
            output_f.write(asctime() + ': ' + 'ConnectionError\n')


bot.polling(none_stop=True, interval=0)