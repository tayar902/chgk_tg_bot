import requests
from bs4 import BeautifulSoup
from time import asctime


def get_all_text():
    all_text = []
    res = requests.get("https://db.chgk.info/random/answers/types1/ \
                           complexity2/795102375/limit1")
    with open('log.txt', 'a') as output_f:
        output_f.write(asctime() + ': ' + str(res) + '\n')
    txt = res.text
    soup = BeautifulSoup(txt, 'html.parser')
    all_text = soup.get_text().split()
    return all_text


i = 0


def get_question(all_text):
    global i
    try:
        res = requests.get("https://db.chgk.info/random/answers/types1/ \
                            complexity2/795102375/limit1")
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            soup.find('div', {'class': 'random_question'}). \
                find('a').text
            tournament = soup.find('div', {'class': 'random_question'}). \
                find('a').text
            question = 'Турнир: ' + str(tournament) + '\n\n' + 'Вопрос:\n'
        except ConnectionError:
            with open('log.txt', 'a') as output_f:
                output_f.write(asctime() + ': ' + 'ConnectionError\n')
        i = 0
    except ConnectionError:
        with open('log.txt', 'a') as output_f:
            output_f.write(asctime() + ': ' + 'ConnectionError\n')
    try:
        all_text[i]
        while True:
            if all_text[i] == 'Вопрос':
                while all_text[i+2] != 'Ответ:':
                    question += all_text[i+2] + ' '
                    i += 1
                break
            i += 1
    except IndexError:
        with open('log.txt', 'a') as output_f:
            output_f.write(asctime() + ': ' + 'IndexError in question\n')
    return question


def get_answer(all_text):
    global i
    outp = ''
    try:
        all_text[i]
        while True:
            if all_text[i] == 'Ответ:':
                try:
                    all_text[i]
                    while (all_text[i] != 'Случайный' and
                           all_text[i + 1] != 'пакет'):
                        outp += all_text[i] + ' '
                        if (all_text[i+1] == 'Комментарий:' or
                            all_text[i+1] == 'Источник(и):' or
                            all_text[i+1] == 'Зачёт:' or
                                all_text[i+1] == 'Автор:' or
                                all_text[i+1] == 'Авторы:'):
                            outp += '\n\n'
                        i += 1
                    break
                except IndexError:
                    with open('log.txt', 'a') as output_f:
                        output_f.write(asctime() + ': ' + 'IndexError\n')
            i += 1
    except IndexError:
        with open('log.txt', 'a') as output_f:
            output_f.write(asctime() + ': ' + 'IndexError\n')
    return outp


get_question(get_all_text())
