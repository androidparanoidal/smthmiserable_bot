# -*- coding: utf-8 -*-
import os
import telebot
import config
from bs4 import BeautifulSoup
from io import BytesIO
import re
import requests
from PIL import Image

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands = ['start'])
def command_start(message):
    bot.send_message(message.chat.id, 'Здравствуй! Я осуществляю поиск изображений. \n Воспользуйся командой /help')

@bot.message_handler(commands = ['help'])
def command_help(message):
    bot.send_message(message.chat.id, 'Чтобы получить изображения, необходимо просто написать ключевые слова.')

@bot.message_handler(content_types = ['text'])
def send_pic(message):
    pictures = find_pictures(message.text, message.chat.id)
    for pic in pictures:
        bot.send_photo(message.chat.id, open(pic, 'rb'))

def find_pictures(query, url):
    way = os.path.abspath(os.curdir)
    way = os.path.join(way, str(url))
    if not os.path.exists(way):
        os.makedirs(way)

    query = query.split()
    query = '+'.join(query)
    query = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
    r = requests.get(query, headers = {'User-Agent': 'Mozilla/5.0 {Windows NT 6.1, WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/43.0.2357.134 Safari/537.36'}, timeout=5)
    get_soup = BeautifulSoup(r.content, 'html.parser')
    pictures = get_soup.find_all('img', {'data-src': re.compile('gstatic.com')})
    pic_way = []

    for n, m in enumerate(pictures[:5]):   #Ты можешь изменить количество желаемых изображений [здесь]
        inf = requests.get(m['data-src'])
        pic = Image.open(BytesIO(inf.content))
        pw = os.path.join(way, str(n) + '.' + pic.format.lower())
        pic.save(pw)
        pic_way.append(pw)

    return pic_way

if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)