import string
from emoji import emojize
from glob import glob
import logging
from random import randint, choice
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import datetime


import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO,
                    filename='bot.log')

def greet_user(update, context):
    #Приветствие пользователя, после вызова команды /start с добавлением эмоджи в приветствен.сообщение
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)        
    update.message.reply_text(f"Привет, пользователь {context.user_data['emoji']}! Ты вызвал команду /start")    


def talk_to_me(update, context): 
    #Эхо-бот, отвечает пользователю той же фразой, которую ввел пользователь. +добавляет эмоджи в конце
    context.user_data['emoji'] = get_smile(context.user_data)     
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(f"{user_text} {context.user_data['emoji']}")


def get_smile(user_data):
    #Выбирает случайный смайл из имеющиегося списка emoji
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']



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
        update.message.reply_text(response) 


def play_random_numbers(user_number):
    #игра с ботом:пользователь вводит число, а бот определяет своё рандомно (+-10 от введенного пользователем)
    # и сравнивает два числа, кто выиграл
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}. Вы выиграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}. Ничья!"
    else:
        message = f"Ваше число {user_number}, моё {bot_number}. Вы проиграли!"
    return message

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
    update.message.reply_text(message)     


def send_cat_picture(update, context):
    #Выбирает картинку(случайную, подходящую по критериям) из имеющихся и отправляет пользователю в ответ на вызов команды /cat
    cat_photos_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, "rb"))


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
    update.message.reply_text(message)


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
    update.message.reply_text(message)



def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", constellation_selection))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("wordcount", word_count_phrase))
    dp.add_handler(CommandHandler('next_full_moon', full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
        

    logging.info("Bot started")

    mybot.start_polling()
    mybot.idle()

if __name__== "__main__":
    main()