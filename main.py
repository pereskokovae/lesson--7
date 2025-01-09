import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv
from functools import partial


def timer(chat_id, text, bot):
    bot.create_timer(parse(text), choose, chat_id=chat_id, text=text, bot=bot)


def choose(chat_id, text, bot):
    bot.send_message(chat_id, "Время вышло!")


def notify_progress(secs_left, chat_id, message_id, text, bot):
    result = parse(text) - secs_left
    update_message = (
        f"""Осталось {secs_left} секунд\n
        {render_progressbar(parse(text), result)}"""
    )
    bot.update_message(chat_id, message_id, update_message)


def create_countdown(chat_id, text, bot):
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    notify_progress_with_bot = partial(notify_progress, bot=bot)
    bot.create_countdown(
        parse(text),
        notify_progress_with_bot,
        chat_id=chat_id,
        message_id=message_id,
        text=text
    )
    timer(chat_id, text, bot)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    load_dotenv()


    tg_token = os.getenv('TG_TOKEN')
    bot = ptbot.Bot(tg_token)
    create_countdown_partial = partial(create_countdown, bot=bot)


    bot.reply_on_message(create_countdown_partial)
    bot.run_bot()


if __name__ == '__main__':
    main()
