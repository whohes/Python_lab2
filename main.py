import telebot
import random

token = '7121960259:AAHO8bj5F-m8LTO5_ojxwpZtLAUwlYz58g0'
bot = telebot.TeleBot(token)

SCORE = 10000

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ \n Чтобы начать викторину, пропиши /quiz ")

QUESTIONS = [
    {
        'text': 'Какая страна в Европе имеет самую низкую плотность населения?',
        'answers': ['Россия', 'Германия', 'Франция', 'Испания'],
        'correct_answer': 'Россия',
    },
    {
        'text': 'Какая планета в Солнечной системе имеет самый длинный год?',
        'answers': ['Марс', 'Нептун', 'Юпитер', 'Сатурн'],
        'correct_answer': 'Нептун',
    },
    {
        'text': 'Самая длинная река?',
        'answers': ['Нил', 'Волга', 'Иртыш', 'Речка-сорочка'],
        'correct_answer': 'Нил',
    },
    {
        'text': 'Какая страна имеет самую большую плотность населения?',
        'answers': ['Индия', 'Китай', 'Индонезия', 'Япония'],
        'correct_answer': 'Китай',
    },
    {
        'text': 'Какой фрукт считается самым калорийным??',
        'answers': ['Авокадо', 'Банан', 'Апельсин', 'Арбуз'],
        'correct_answer': 'Авокадо',
    },
]

ALL_QUESTIONS = QUESTIONS.copy()

@bot.message_handler(func=lambda message: message.text == '/quiz')
def generate_question(message):
    global QUESTIONS
    if not QUESTIONS:
        QUESTIONS = ALL_QUESTIONS.copy()
    question = random.choice(QUESTIONS)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for answer in question['answers']:
        keyboard.add(telebot.types.KeyboardButton(answer))
    bot.send_message(message.chat.id, f"ВОПРОСИК:\n{question['text']}", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in [answer for question in QUESTIONS for answer in question['answers']])
def check_answer(message):
    global SCORE, QUESTIONS

    for question in QUESTIONS:
        if message.text == question['correct_answer']:
            bot.reply_to(message, "Правильно!")
            SCORE = SCORE * 10
            bot.reply_to(message, SCORE)
            QUESTIONS.remove(question)
            if QUESTIONS:
                generate_question(message)
            else:
                bot.send_message(message.chat.id, "Викторина окончена!")
            return

    bot.reply_to(message, "Неверный ответ. Викторина начинается заново, Ваши очки сбрасываются. \n Чтобы начать заново, пропишите /quiz ")
    QUESTIONS = ALL_QUESTIONS.copy()
    SCORE = 10000

bot.polling()