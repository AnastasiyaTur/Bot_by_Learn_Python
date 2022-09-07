import logging
from urllib import response
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import ephem
import datetime
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO,
                    filename='bot.log')

def greet_user(update, context):
    print('Вызван /start')    
    update.message.reply_text('Привет пользователь! Ты вызвал команду /start')


def talk_to_me(update, context):     
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def constellation_selection(update, context):
    planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']        
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
    


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", constellation_selection))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
        

    logging.info("Bot started")

    mybot.start_polling()
    mybot.idle()

if __name__== "__main__":
    main()