import requests
from bs4 import BeautifulSoup
from time import asctime


def get_soup():
    url = ("https://db.chgk.info/random/answers/types1/" +
           "complexity2/795102375/limit1")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def get_all_text(soup):
    all_text = []
    all_text = soup.get_text().split()
    return all_text


i = 0


def get_question(all_text, soup):
    global i
    question = ''
    try:
        soup.find('div', {'class': 'random_question'}). \
            find('a').text
        tournament = soup.find('div', {'class': 'random_question'}). \
            find('a').text
        question = 'Турнир: ' + str(tournament) + '\n\n' + 'Вопрос:\n'
    except AttributeError:
        print(asctime() + ': ' + 'AttributeError in get_question\n')
    i = 0
    try:
        img_html = soup.find('img')
        img = img_html['src']
        if img[0:6] == 'https:':
            question += img + '\n'
    except requests.exceptions.MissingSchema:
        question += ''
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
        print(asctime() + ': ' + 'IndexError in get_question\n')
    return question


def get_answer(all_text):
    global i
    answer = ''
    try:
        while True:
            if all_text[i] == 'Ответ:':
                while (all_text[i][-1] != '.' and
                        all_text[i+1] != 'Комментарий:' and
                        all_text[i+1] != 'Источник(и):' and
                        all_text[i+1] != 'Автор:' and
                        all_text[i+1] != 'Авторы:' and
                        all_text[i+1] != 'Зачёт:' and
                        all_text[i+1] +
                        all_text[i+2] != 'Случайныйпакет'):
                    answer += all_text[i+1] + ' '
                    i += 1
                break
            i += 1
    except IndexError:
        print(asctime() + ': ' + 'IndexError in get_answer\n')
    return answer


def get_comment(all_text):
    comment = ''
    global i
    try:
        while True:
            if all_text[i] == 'Комментарий:' or all_text[i] == 'Источник(и):':
                while (all_text[i] +
                        all_text[i+1] != 'Случайныйпакет'):
                    comment += all_text[i] + ' '
                    if (all_text[i+1] == 'Источник(и):' or
                        all_text[i+1] == 'Зачёт:' or
                        all_text[i+1] == 'Автор:' or
                            all_text[i+1] == 'Авторы:'):
                        comment += '\n\n'
                    i += 1
                break
            i += 1
    except IndexError:
        print(asctime() + ': ' + 'IndexError in get_comment\n')
    return comment
