import requests
from yobit import get_btc
from translate import get_translate

#https://api.telegram.org/bot484689969:AAEjgfcR7__nCrxfAyOpAqQqscvI9DL-5mM/sendmessage?chat_id=475425006&text=hi
token = '484689969:AAEjgfcR7__nCrxfAyOpAqQqscvI9DL-5mM'
URL = 'https://api.telegram.org/bot' + token + '/'


# global last_update_id
last_update_id = 0


def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()
    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id

    if last_update_id != current_update_id:
        last_update_id = current_update_id

        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']

        message = {'chat_id' : chat_id,
                   'text' : message_text }
        return message
    return None


def send_message(chat_id, text='Wait a second please...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def run():
    while True:
        answer = get_message()
        if answer is not None:
            chat_id = answer['chat_id']
            text = answer['text']

            # пытаюсь разобраться с переводчиком!!!
            # Проверка на команда /btc узнаем курс биткоина
            if text.startswith('/'):

                if text == '/btc':
                    send_message(chat_id, get_btc())
                elif text == '/help':  # проверка на команду /help Выдаем список всех команд для бота
                    send_message(chat_id, '/btc - Узнать курс Биткоина на бирже yobit.net\n'
                                          '/translate - Через данную команду можно перевести любой вводимы текст с английского на русский')
                elif '/translate ' in text:
                    text_translate = text.replace('/translate ', '') # Вырезаем слово /translate
                    text_translate = get_translate(text_translate)

                    send_message(chat_id, text_translate)  # пишем перевод
                else:  # при получение любого иного текста выскакивает эта фраза
                    send_message(chat_id, 'Я тебя не понимаю;)')
        else:
            continue
