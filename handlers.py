from glob import glob
import os
from random import choice

import datetime
import ephem
import string

from db import (db, get_or_create_user, subscribe_user, unsubscribe_user,
                save_cat_image_vote, user_voted, get_image_rating)
from jobs import alarm
from utils import (play_random_numbers, get_bot_number, main_keyboard,
                   has_object_on_image, cat_rating_inline_keyboard)


def greet_user(update, context):
    # Приветствие пользователя, после вызова команды /start
    # с добавлением эмоджи в приветствен.сообщение
    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    print('Вызван /start')
    update.message.reply_text(
        f"Привет, пользователь {user['emoji']}! Ты вызвал команду /start",
        reply_markup=main_keyboard()
    )


planets = [x[2] for x in ephem._libastro.builtin_planets()]
def constellation_selection(update, context):
    # Определяет в каком созвездии планета (вводит пользователь)
    # в текущую дату и время

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    user_text = update.message.text.split()[1]
    planet = user_text
    if planet in planets:
        planet_now = getattr(ephem, planet)(datetime.datetime.now())
        constellation = ephem.constellation(planet_now)
        response = f"{planet} is now in the constellation {constellation}"
        update.message.reply_text(response)
    else:
        response = f"{planet} is not a planet"
        update.message.reply_text(response, reply_markup=main_keyboard())


def talk_to_me(update, context):
    # Эхо-бот, отвечает пользователю той же фразой, которую ввел пользователь.
    # +добавляет эмоджи в конце

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(f"{user_text} {user['emoji']}",
                              reply_markup=main_keyboard())


def guess_number(update, context):
    # Игра с ботом (play_random_numbers). Определяет здесь своё рандомное число

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    if context.args:
        try:
            user_number = int(context.args[0])
            bot_number = get_bot_number(user_number)
            message = play_random_numbers(user_number, bot_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message, reply_markup=main_keyboard())


def send_cat_picture(update, context):
    # Выбирает картинку(случайную, подходящую по критериям) из имеющихся
    # и отправляет пользователю в ответ на вызов команды /cat

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    cat_photos_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    if user_voted(db, cat_photo_filename, user['user_id']):
        rating = get_image_rating(db, cat_photo_filename)
        keyboard = None
        caption = f"Рейтинг картинки {rating}"
    else:
        keyboard = cat_rating_inline_keyboard(cat_photo_filename)
        caption = None
    context.bot.send_photo(chat_id=chat_id,
                           photo=open(cat_photo_filename, "rb"),
                           reply_markup=keyboard,
                           caption=caption)


def word_count_phrase(update, context):
    # Считает количество слов в введенной фразе, убирая в ней все элементы
    # пунктуации. Отвечает пользователю сколько слов он ввёл

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    if context.args:
        try:
            # Введенный текст превращаем в строку
            user_text = ' '.join(context.args)
            # Убираем все знаки пунктуации, чтобы они не считались за символ
            user_text = user_text.translate(str.maketrans('', '', string.punctuation))
            # Считаем количество слов в получившейся строке
            user_text = len(user_text.split())
            message = f"Phrase consists of {user_text} words."

        except (TypeError, ValueError):
            message = "Please, enter the correct phrase!"
    else:
        message = "Enter your phrase."
    update.message.reply_text(message, reply_markup=main_keyboard())


def full_moon(update, context):
    # Определяет, когда ближайшее полнолуние(пользователь вводит дату)

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    if context.args:
        try:
            enter_date = '-'.join(context.args)
            next_moon = ephem.next_full_moon(enter_date)
            message = f"Ближайшее полнолуние: {next_moon}"
        except (TypeError, ValueError):
            message = "Пожалуйста, введите дату в формате: год-месяц-день"
    else:
        message = "Пожалуйста, введите интересующую дату в формате: год-месяц-день"
    update.message.reply_text(message, reply_markup=main_keyboard())


def user_coordinates(update, context):
    # Выводит локацию, где находится пользователь

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}!",
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    # Распознавание на фото котов и сохранение данной картинки

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    update.message.reply_text('Обрабатываем фото')
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{update.message.photo[-1].file_id}.jpg')
    photo_file.download(file_name)
    update.message.reply_text('Файл сохранен')
    if has_object_on_image(file_name, 'cat'):
        update.message.reply_text('Обнаружен котик, сохраняю в библиотеку')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Котик не обнаружен!')


def subscribe(update, context):
    # Подписка на рассылку сообщений в чате

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('Вы успешно подписались!')


def unsubscribe(update, context):
    # Отписка на рассылку сообщений в чате

    user = get_or_create_user(db,
                              update.effective_user,
                              update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('Вы успешно отписались!')


def set_alarm(update, context):
    # Установка уведомлений от бота по времени

    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm,
                                   alarm_seconds,
                                   context=update.message.chat.id)
        update.message.reply_text(f'Уведомление через {alarm_seconds} секунд')
    except (ValueError, TypeError):
        update.message.reply_text('Введите целое число секунд после команды')


def cat_picture_rating(update, context):
    # Отражение рейтинга (после голосования) конкретной картинки кота

    update.callback_query.answer()
    callback_type, image_name, vote = update.callback_query.data.split("|")
    vote = int(vote)
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    save_cat_image_vote(db, user, image_name, vote)
    rating = get_image_rating(db, image_name)
    update.callback_query.edit_message_caption(caption=f"Рейтинг картинки {rating}")
