from config import tg_bot_token,open_weather_token
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests
#BotFather
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

#Первая команда
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Напишите название города")

#Вывод всех данных, проверка общая
@dp.message_handler()
async def get_weather(message: types.Message):
    try: #api погоды
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
    #отбор нужных данных из json
        city = data["name"]
        cur_weather = data["main"]["temp"]
        wind = data["wind"]["speed"]

        await message.reply(
            f"Погода в городе: {city}\nТемпература: {cur_weather}C\nСкорость ветра: {wind}м/c"
        )
        # отправление рандомных фото собак
        chat_id = message.chat.id
        await bot.send_photo(chat_id, photo=requests.get('https://random.dog/woof.json').json()['url'])
        # курсы двух валют к рублю на текущее время
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        if response.status_code == 200:
            content = response.json()
            dol = content["Valute"]["USD"]["Value"]
            eur = content["Valute"]["EUR"]["Value"]
            await message.reply(f"Доллары США: {dol} руб.\nЕвро: {eur} руб.\n")

    except:
        await message.reply("Проверьте название города")


if __name__ == '__main__':
    executor.start_polling(dp)
