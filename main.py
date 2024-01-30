from datetime import datetime, timedelta
import requests
import telebot
from random import choice
from wait_messages import wait_messages


# bot setting
bot = telebot.TeleBot("your bot token")
timeout = 1
next_joke_time = datetime.now()

# parser settings
joke_api_link = "http://castlots.org/generator-anekdotov-online/generate.php"
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en,ru;q=0.9,en-US;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Host": "castlots.org",
    "Origin": "https://castlots.org",
    "Referer": "https://castlots.org/generator-anekdotov-online/",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def get_random_joke():
    response = requests.get(joke_api_link, headers=headers)

    match response.status_code:
        case 200:
            return response.json()['va']
        case code:
            return f"Ошибка сервера с анекдотами {code}, данные запроса {response.json()}"

    return response.json()


def generate_joke_message(chat_id):
    global next_joke_time
    time_now = datetime.now()
    if next_joke_time <= time_now:
        joke = get_random_joke()
        bot.send_message(chat_id, joke)
        next_joke_time = time_now + timedelta(seconds=timeout)
    else:
        bot.send_message(chat_id, ''.join((choice(wait_messages), f"\nПожалуйста подождите еще {round(next_joke_time.timestamp() - time_now.timestamp())} секунд.")))


@bot.message_handler(commands=["start"])
def handle_start(message):
    pass


@bot.message_handler(content_types=["text"])
def handle_text(message):
    match message.text.lower():
        case "спиздани шутку":
            generate_joke_message(message.chat.id)
        case _:
            pass


if __name__ == '__main__':
    bot.polling()
