from utils import get_bot_number, play_random_numbers


def test_get_bot_number():
    user_number = 10
    assert (user_number - 10) <= get_bot_number(user_number) <= (user_number + 10)


def test_play_random_numbers_win():
    user_number = 10
    bot_number = 5
    assert play_random_numbers(user_number, bot_number) == "Ваше число 10, моё 5. Вы выиграли!"


def test_play_random_numbers_lose():
    user_number = 5
    bot_number = 10
    assert play_random_numbers(user_number, bot_number) == "Ваше число 5, моё 10. Вы проиграли!"


def test_play_random_numbers_equal():
    user_number = 10
    bot_number = 10
    assert play_random_numbers(user_number, bot_number) == "Ваше число 10, моё 10. Ничья!"
