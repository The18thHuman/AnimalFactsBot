""" Модуль, содержащий 'бизнес-логику' AnimalFactsBot."""
import json
import logging
import tempfile
from io import BytesIO

import requests
from PIL import Image
from aiogram.types import FSInputFile, URLInputFile
from googletrans import Translator
from langcodes import Language


def get_cat_fact(language: str):
    """ Получить случайный факт о кошках из API."""
    # Так как aiogram предоставляет 2-х символьные коды языка,
    # а API требует 3-х символьные, конвертируем их.
    code_3_letter = Language.get(language).to_alpha3()
    url = f'https://meowfacts.herokuapp.com/?lang={code_3_letter}'
    response = requests.get(url, timeout=10)
    data = response.json()
    return data['data'][0]


def get_cat_picture():
    """ Получить картинку случайной кошки из API."""
    url = 'https://cataas.com/cat'
    response = requests.get(url, timeout=10)
    # API в ответ на get запрос предоставляет картинку в формате jpeg.
    # Чтобы отправить её в телеграмме сохраняем её во временный файл.
    image = Image.open(BytesIO(response.content))
    # Картинка предоставлена в формате RGBA, который не поддерживается jpeg.
    # Поэтому конвертируем её в RGB, убирая прозрачность, которая почему-то
    # там есть (?).
    rgb_im = image.convert('RGB')
    with tempfile.NamedTemporaryFile() as fp:
        filename = f'{fp.name}.jpeg'
        rgb_im.save(filename, 'jpeg')
        # Перед отправкой необходимо создать объект класса FSInputFile для
        # корректного распознавания фото aiogram-ом.
        photo = FSInputFile(filename)
        return photo


def get_dog_fact(language: str):
    """Получить случайный факт о собаках из API."""
    url = 'https://dogapi.dog/api/v2/facts'
    response = requests.get(url, timeout=10)
    data = response.json()
    # Так как API не поддерживает многоязычность,
    # переводим полученный факт с помощью
    # переводчика google.
    translator = Translator()
    text = data['data'][0]['attributes']['body']
    fact = translator.translate(text, dest=language)
    return fact.text


def get_dog_picture():
    """ Получить случайную картинку собаки из API."""
    url = 'https://dog.ceo/api/breeds/image/random'
    # Возможные форматы изображений для запроса ниже.
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
    # В использованном API существует проблема того, что ссылка на случайное изображение
    # возвращает 404, т.е. картинка не существует.
    # Однако, нам нужно все равно её отправить. Поэтому мы отправляем картинку только в случае
    # если полученная нами ссылка валидна и возвращает 200 с header корректного типа
    # изображения. Если мы получаем 404, то пробуем снова с другой картинкой.
    while True:
        response = requests.get(url, timeout=10)
        image_link = json.loads(response.text)['message']
        r = requests.head(image_link, timeout=10)
        if r.status_code == 200 and r.headers["content-type"] in image_formats:
            photo = URLInputFile(image_link)
            return photo

        logging.info(msg=f'Image {image_link} not found.')
