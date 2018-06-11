import requests


def get_translate(text=''):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?lang=en-ru&key=trnsl.1.1.20180218T101426Z.cce41916431b11ed.9428fdf2e11172d4dce13ef03f157ea7d9bc6477&text={text}'.format(
        text=text
    )
    translate = requests.get(url).json()
    print(translate)
    return translate['text'][0]


# get_translate()