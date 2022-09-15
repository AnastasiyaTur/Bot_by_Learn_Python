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
    print('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)        
    update.message.reply_text(f"Привет, пользователь {context.user_data['emoji']}! Ты вызвал команду /start")    


def talk_to_me(update, context): 
    context.user_data['emoji'] = get_smile(context.user_data)     
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(f"{user_text} {context.user_data['emoji']}")


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']



planets = [x[2] for x in ephem._libastro.builtin_planets()]

def constellation_selection(update, context):            
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
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}. Вы выиграли!"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}. Ничья!"
    else:
        message = f"Ваше число {user_number}, моё {bot_number}. Вы проиграли!"
    return message

def guess_number(update, context):
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
    cat_photos_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, "rb"))


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", constellation_selection))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
        

    logging.info("Bot started")

    mybot.start_polling()
    mybot.idle()

if __name__== "__main__":
    main()