import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import (greet_user, constellation_selection, guess_number, word_count_phrase,
                       full_moon, send_cat_picture, user_coordinates, talk_to_me) 
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO,
                    filename='bot.log')




def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", constellation_selection))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(CommandHandler("wordcount", word_count_phrase))
    dp.add_handler(CommandHandler('next_full_moon', full_moon)) 
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))  
    dp.add_handler(MessageHandler(Filters.location, user_coordinates)) 
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
        

    logging.info("Bot started")

    mybot.start_polling()
    mybot.idle()

if __name__== "__main__":
    main()