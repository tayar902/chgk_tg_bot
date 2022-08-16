import telebot
from telebot import types
from time import asctime
import chgk_api
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


bot = telebot.TeleBot('5420233585:AAFUeq6tn5a-DG3FkgqYEYEUF6aqR-MDoTM')


@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вопрос ЧГК")
    markup.add(item1)
    bot.send_message(m.chat.id, 'Нажмите: \nВопрос ЧГК для получения вопроса',
                     reply_markup=markup)


answer = ''
comment = ''
check_input = []


@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        all_text = chgk_api.get_all_text()
        outp_message = ''
        question = ''
        global answer
        global comment
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        check_input.append(message.text.strip().lower())
        print(check_input)
        print(similar(answer.lower(), message.text.strip().lower()))
        if message.text.strip().lower() == 'вопрос чгк':
            item2 = types.KeyboardButton("Ответ")
            markup.add(item2)
            if check_input == ['вопрос чгк']:
                question = chgk_api.get_question(all_text)
                answer = chgk_api.get_answer(all_text)
                comment = chgk_api.get_comment(all_text)
                outp_message = question
                bot.send_message(message.chat.id, outp_message,
                                 reply_markup=markup)
            else:
                del check_input[0]
            bot.send_message(message.chat.id, 'Напишите ответ или' +
                             ' Нажмите "Ответ", чтобы '
                             + 'получить ответ')
        elif message.text.strip().lower() == 'ответ':
            item1 = types.KeyboardButton("Вопрос ЧГК")
            markup.add(item1)
            if check_input == ['вопрос чгк', 'ответ']:
                outp_message = ('Ответ: ' + answer + '\n\n' + comment)
            else:
                outp_message = 'Вы не запросили вопрос!'
            check_input.clear()
            bot.send_message(message.chat.id, outp_message,
                             reply_markup=markup)
        elif similar(answer.lower(), message.text.strip().lower()) >= 0.7:
            item1 = types.KeyboardButton("Вопрос ЧГК")
            markup.add(item1)
            check_input.clear()
            bot.send_message(message.chat.id, 'Абсолютно верно!' + '\n\n' +
                             comment,
                             reply_markup=markup)
        else:
            if check_input[0] == 'вопрос чгк':
                bot.send_message(message.chat.id, 'Ответ неверный :(\n')
            else:
                bot.send_message(message.chat.id, 'Вы ввели незнакомую команду'
                                 + '\nНажмите "Вопрос ЧГК" для получения '
                                 + 'вопроса')
            del check_input[-1]
    except ConnectionError:
        with open('log.txt', 'a') as output_f:
            output_f.write(asctime() + ': ' + 'ConnectionError\n')


bot.polling(none_stop=True, interval=0)
