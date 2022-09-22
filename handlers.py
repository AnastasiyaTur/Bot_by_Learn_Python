from glob import glob
from random import choice

import datetime
import ephem
import string

from utils import get_smile, play_random_numbers, main_keyboard


def greet_user(update, context):
    #Приветствие пользователя, после вызова команды /start с добавлением эмоджи в приветствен.сообщение
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)         
    update.message.reply_text(
        f"Привет, пользователь {context.user_data['emoji']}! Ты вызвал команду /start",
        reply_markup = main_keyboard()
    )  


planets = [x[2] for x in ephem._libastro.builtin_planets()]
def constellation_selection(update, context):   
    #Определяет в каком созвездии планета (вводит пользователь) в текущую дату и время         
    user_text = update.message.text.split()[1]
    planet = user_text
    if planet in planets:
        planet_now = getattr(ephem, planet)(datetime.datetime.now())
        constellation = ephem.constellation(planet_now)
        response = f"{planet} is now in the constellation {constellation}"
        update.message.reply_text(response)
    else:
        response = f"{planet} is not a planet"
        update.message.reply_text(response, reply_markup = main_keyboard())  


def talk_to_me(update, context): 
    #Эхо-бот, отвечает пользователю той же фразой, которую ввел пользователь. +добавляет эмоджи в конце
    context.user_data['emoji'] = get_smile(context.user_data)     
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(f"{user_text} {context.user_data['emoji']}", reply_markup = main_keyboard())


def guess_number(update, context):
    #игра с ботом (play_random_numbers). Определяет здесь своё рандомное число
    print(context.args)
    if context.args:
        try:            
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup = main_keyboard()) 


def send_cat_picture(update, context):
    #Выбирает картинку(случайную, подходящую по критериям) из имеющихся и отправляет пользователю в ответ на вызов команды /cat
    cat_photos_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, "rb"), reply_markup = main_keyboard())


def word_count_phrase(update, context):
    #Считает количество слов в введенной фразе, убирая в ней все элементы пунктуации. Отвечает пользователю сколько слов он ввёл
    print(context.args)        
    if context.args:
        try:            
            user_text = ' '.join(context.args) #Введенный текст превращаем в строку
            user_text = user_text.translate(str.maketrans('', '', string.punctuation)) #Убираем все знаки пунктуации, чтобы они не считались за символ/слово
            user_text = len(user_text.split())   #Считаем количество слов в получившейся строке         
            message = f"Phrase consists of {user_text} words."
                
        except (TypeError, ValueError):
            message = "Please, enter the correct phrase!"
    else:
        message = "Enter your phrase."
    update.message.reply_text(message, reply_markup = main_keyboard())


def full_moon(update, context):
    #Определяет, когда ближайшее полнолуние(пользователь вводит дату)
    print(context.args)
    if context.args:
        try:
            enter_date = '-'.join(context.args)
            next_moon = ephem.next_full_moon(enter_date)
            message = f"Ближайшее полнолуние: {next_moon}"
        except (TypeError, ValueError):
            message = "Пожалуйста, введите дату в формате: год-месяц-день"
    else:
        message = "Пожалуйста, введите интересующую дату в формате: год-месяц-день"
    update.message.reply_text(message, reply_markup = main_keyboard())


def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data) 
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup = main_keyboard()
    )
