import time
import requests
import base64
from random import randint
from config import TELEGRAM_TOKEN
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def func_start(message: types.Message):
    await message.answer('Привет я нейронка для изображений на минималках')
def general_img(promt_text):
    promt = {
        "modelUri": "art://b1g3f13cj7d6d3ss2md9/yandex-art/latest",
        "generationOptions": {
          "seed": randint(100, 1000000)
        },
        "messages": [
          {
            "weight": 1,
            "text": promt_text
          }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "API-Key AQVNyLYVXNp70b6KNtOJbHsj-aV2vvHaHfmZcp95"
    }

    response = requests.post(url = url, headers = headers, json= promt)
    result = response.json()
    print(result)

    operator_id = result['id']

    operator_url = f"https://llm.api.cloud.yandex.net:443/operations/{operator_id}"

    while True:
        operator_response = requests.get(operator_url, headers = headers)
        operator_result = operator_response.json()
        if 'response' in operator_result:
            image_base54 = operator_result['response']['image']
            image_data = base64.b64decode(image_base54)
            return image_data
        else:
            time.sleep(5)

@dp.message_handler()
async def hendle_message(message: types.Message):
    user_text = message.text
    await message.reply('Идет генерация, подождите')
    try:
        image_data = general_img(user_text)
        await message.reply_photo(photo=image_data)
    except Exception as e:
        await message.reply(f'Произошла ошибка {e}')

    #         break
    #     else:
    #         print('Изображение еще не готово')
    #         time.sleep(5)
    # image_data = base64.b64decode(image_base54)
    # with open('image.jpeg', 'wb') as image_file:
    #     image_file.write(image_data)
    #
    # print('Изображение готово, смотри результат')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)