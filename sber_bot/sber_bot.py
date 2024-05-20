import telebot
from telebot import types
import json

TOKEN = '7099301710:AAFePlrn29N-Diwq-uPMcjLTrHI3qab9BIY'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Отдыхающий')
    itembtn2 = types.KeyboardButton('Путешественник')
    itembtn3 = types.KeyboardButton('Экстремал')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Мы рады Вас приветствовать в нашем боте! Выберите вариант страховки:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    inl_markup = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton('Да', callback_data='chose_option1')
    deny_button = types.InlineKeyboardButton('Нет', callback_data='chose_option_more2')

    inl_markup.row(confirm_button, deny_button)

    if message.text == 'Отдыхающий':
        with open('rest_discr.txt', 'r', encoding="utf-8") as f:
            text = f.read()

        bot.send_photo(message.chat.id, open('resting.jpg', 'rb'), caption="Вы выбрали тариф Отдыхающий")
        bot.send_message(message.chat.id, text, parse_mode= "Markdown")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEMFi9mPlGN0nQWHkFASOIVuQggXCLyQQAClyMAAulVBRjV9Db5MvEE6TUE')

        bot.send_message(message.chat.id, 'Вы готовы выбрать тариф?', reply_markup=inl_markup)

    elif message.text == 'Путешественник':
        with open('trav_discr.txt', 'r', encoding="utf-8") as f:
            text = f.read()

        bot.send_photo(message.chat.id, open('traveller.jpg', 'rb'), caption="Вы выбрали тариф Путешественник")
        bot.send_message(message.chat.id, text[:], parse_mode="Markdown")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEMFjFmPlGZbiFQGRce8iAT_HBocBzp3AACww8AAk_RiUgz6-CYWUcJBTUE')

        bot.send_message(message.chat.id, 'Вы готовы выбрать тариф?', reply_markup=inl_markup)

    elif message.text == 'Экстремал':
        with open('exstr_discr.txt', 'r', encoding="utf-8") as f:
            text = f.read()

        bot.send_photo(message.chat.id, open('extreme.jpg', 'rb'), caption="Вы выбрали тариф Экстремал")
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEMFi1mPlGD4jqeBuafXYYTMGDt3_t6JgACEhAAAgrjiEjhdLOxvTUJgzUE')

        bot.send_message(message.chat.id, 'Вы готовы выбрать тариф?', reply_markup=inl_markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('chose'))
def option_choice(call):
    if call.data[-1] == '1':
        option_markup = types.InlineKeyboardMarkup()
        travel_button = types.InlineKeyboardButton('Путешественник', callback_data='oПутешественник1')
        resting_button = types.InlineKeyboardButton('Отдыхающий', callback_data='oОтдыхающий2')
        exctreme_button = types.InlineKeyboardButton('Экстремал', callback_data='oЭкстремал3')

        option_markup.row(resting_button, travel_button, exctreme_button)

        bot.send_message(call.message.chat.id, 'Какой тариф вы выбрали?', reply_markup=option_markup)
    elif call.data[-1] == '2':
        bot.send_message(call.message.chat.id, 'В таком случае посмотрите остальные тарифы! Они доступны по кнопкам.')

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('o'))
def registration(call):
    msg = bot.send_message(call.message.chat.id, 'Мы рады, что вы нашли подходящее предложение! Пожалуйста, отправьте свои данные в следующем формате:\n\n'
                                                 'ФИО\nдата рождения (00.00.0000)\nпол (М, Ж)\n\n'
                                                 '*Обращаем внимание:*\nпереходя по ссылке вы соглашаетесь на обработку персональных данных.',
                                                parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, person_data)

    bot.answer_callback_query(call.id)

def person_data(message):
    p_data = message.text.split('\n')
    name, birth_date, gender= p_data[0], p_data[1], p_data[2]
    d = {
        'Имя': name,
        "Дата рождения": birth_date,
        "Пол": gender
    }

    with open("personal data.json", "a", encoding="utf-8") as file:
        json.dump(d, file)

    bot.send_message(message.chat.id, 'Спасибо! Для дальнейшего оформления страховки просим вас отправить свои паспотрные данные. '
                                      'Пройдите по ссылке и следуйте инстуркициям: @Passport_pix_bot')

bot.polling(none_stop=True)