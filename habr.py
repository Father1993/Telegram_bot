import requests
import telebot
import random
from telebot import types
from bs4 import BeautifulSoup

url = "https://habr.com/ru/news/"
API_KEY = "6224719907:AAFhsVDHrjGMhAmEg920LCMdH9aay2iQmjQ"
url2 = "https://www.gismeteo.ru/weather-khabarovsk-4862/"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}

proxies = {"https": f"http://YemFds:2d6wdt@194.67.218.216:9101"}


def parser(url):
    req = requests.get(url, headers=headers, proxies=proxies)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    all_news_hrefs = soup.find_all(class_="tm-title__link")
    return all_news_hrefs


list_news = []
for item in parser(url):
    item_text = item.text
    item_href = "https://habr.com" + item.get("href")
    all_news = f"Свежак: {item_href}"
    list_news.append(all_news)


random.shuffle(list_news)
# print(list_news)

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(
        message.chat.id,
        "Привет, чтобы узнать свежие и популярные новости с сайта Harb.com. Введите: /news или нажмите на кнопку",
        reply_markup=keyboard(),
    )


@bot.message_handler(content_types=["text"])
def popular_news(message):
    if message.text == "NEWS":
        bot.send_message(message.chat.id, list_news[0], reply_markup=keyboard())
        del list_news[0]


def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton("NEWS")
    btn2 = types.KeyboardButton("Узнать погоду")
    markup.add(btn1)
    return markup


bot.polling()
