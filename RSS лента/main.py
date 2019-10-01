import telebot
import requests
from bs4 import BeautifulSoup
import re

bot = telebot.TeleBot('961998122:AAFwHfsHfhn1y9hnvrQ4ZyQcSOVXgahfi0I')


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        global k
        bot.send_message(message.chat.id, "Отправьте мне ссылку на RSS ленту: " + "\n\n" +
                         "Список популярных RSS лент: " + "\n" + "Лента ру - http://lenta.ru/l/r/EX/import.rss" + "\n" +
                         "СПОРТ сегодня - http://www.sports.ru/sports_docs.xml" + "\n" +
                         "Travel ru -  http://www.travel.ru/inc/side/yandex.rdf")
        k = 0
    except:
        bot.send_message(message.chat.id, "Возникла ошибка.")


@bot.message_handler(commands=['help'])
def get_help(message):
    try:
        bot.send_message(message.chat.id, "Бот создан для просмотра новостей"
                                          " с помощью специальных RSS лент. Введите /start для начала пользования.")
    except:
        bot.send_message(message.chat.id, "Error")


@bot.message_handler(content_types=['text'])
def start_message(message):
    a = 0
    try:
        global k, url
        if k == 0:
            url = message.text
            bot.send_message(message.chat.id, "Сообщите пару ключевых слов: " +
                             "\n\n" +
                             "например: Трамп, Зеленский, сообщил")
            k += 1

        else:
            category = message.text
            resp = requests.get(url)
            soup = BeautifulSoup(resp.content, features='xml')
            items = soup.findAll('item')
            key_words = category
            for item in items:
                for k in key_words.split(","):
                    if (k.lower() in " ".join([i.lower() for i in item.title.text.split()])) or (
                            k.lower() in " ".join([i.lower() for i in cleanhtml(item.description.text).split()])):
                        a += 1
                        bot.send_message(message.chat.id,
                                         item.title.text +
                                         "\n" +
                                         cleanhtml(item.description.text))

            if a == 0:
                bot.send_message(message.chat.id, "По данному запросу новостей нема")
            k = 0
    except:
        bot.send_message(message.chat.id, "Произошла ошибка. Возможно вы ввели неверные данные. "
                                          "Повторите попытку позже.")


bot.polling()
