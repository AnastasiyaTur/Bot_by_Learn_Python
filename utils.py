from emoji import emojize
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

#Выбирает случайный смайл из имеющиегося списка emoji
def get_smile(user_data):    
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']


#игра с ботом:пользователь вводит число, а бот определяет своё рандомно (+-10 от введенного пользователем)
# и сравнивает два числа, кто выиграл
def play_random_numbers(user_number):    
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}. Вы выиграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}. Ничья!"
    else:
        message = f"Ваше число {user_number}, моё {bot_number}. Вы проиграли!"
    return message


#Создаёт две кнопки на клавиатуре
def main_keyboard():
    return ReplyKeyboardMarkup([['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]])