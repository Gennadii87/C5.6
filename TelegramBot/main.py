import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges, KEY, val1, val2, col
import traceback
import requests
import datetime

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Привет, Я бот - конвертер валют! помощь - /help\nсписок валют - /values\nбыстрая команда - /exchange "
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = "Пример запроса для получения курса валют: рубль доллар 1"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(commands=['exchange'])
def send_exchange_rate(message):
    result = exchange_rate()
    bot.send_message(chat_id=message.chat.id, text=result)


def exchange_rate():
    url = f'https://api.apilayer.com/exchangerates_data/convert?to={val1}&from={val2}&amount={col}'
    response = requests.get(url, headers=KEY)
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data['result']
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        message = f"{col} {val2} = {exchange_rate} {val1} на {date}"
    else:
        message = "Ошибка получения курса валют"
    return message


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
