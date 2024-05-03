import telebot
import webbrowser
import sqlite3
from telebot import types

number = None

bot = telebot.TeleBot('7031734423:AAHVWVCcLHuWG4ifFS9pXE4I-_HlvZbrKtk')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Сюда Вы можете отправить фото автомобиля, который сильно загрязняет воздух!')
    bot.send_message(message.chat.id,f'{message.from_user.first_name}, отправьте фото автомобиля так, чтобы было видно номер')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    # conn = sqlite3.connect('badmobile.sql')
    # cur = conn.cursor()
    # cur.execute('CREATE TABLE IF NOT EXISTS badmobile (id int auto_increment PRIMARY KEY, logitude varchar, latitude varchar, number text)')
    # conn.commit()
    # cur.close()
    # conn.close()
    bot.reply_to(message, 'Отправьте номер машины в формате: 111AAA01')
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    tx = message.text.lower()
    if len(tx) == 8 and tx[0:3].isnumeric() and not tx[3].isnumeric() and not tx[4].isnumeric() and not tx[5].isnumeric() and tx[6:8].isnumeric():
        global number
        number = tx
        bot.reply_to(message, 'Спасибо! Вы помогаете городу!')
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Отправьте местоположение автомобиля!", reply_markup=keyboard)

    elif len(tx) == 7 and tx[0:3].isnumeric() and not tx[3].isnumeric() and not tx[4].isnumeric() and tx[5:7].isnumeric():
        number = tx
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Отправьте местоположение автомобиля!", reply_markup=keyboard)

    else:
        bot.reply_to(message, 'Формат номера неверный! Отправьте номер машины в формате: 111AAA01')
        bot.register_next_step_handler(message, on_click)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        # conn = sqlite3.connect('badmobile.sql')
        # cur = conn.cursor()
        # cur.execute("INSERT INTO badmobile (logitude, latitude, nubmer) VALUES ('%s','%s','%s')" % (message.location.longitude, message.location.latitude, number))
        # conn.commit()
        # cur.close()
        # conn.close()
        bot.send_message(message.chat.id, "Спасибо, что помогаете городу!")
@bot.message_handler()
def get_text(message):
    bot.reply_to(message, 'Для начала отправьте фото автомобиля')

bot.polling(none_stop=True)