import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv


def timer(chat_id, text):
    bot.create_timer(parse(text), choose, chat_id=chat_id, text=text)


def choose(chat_id, text):
    bot.send_message(chat_id, "Время вышло!")


def create_countdown(chat_id, text):
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    bot.create_countdown(
            parse(text),
            notify_progress,
            chat_id=chat_id,
            message_id=message_id,
            text=text
    )
    timer(chat_id, text)


def notify_progress(secs_left, chat_id, message_id, text):
    result = parse(text)-secs_left
    update_message = (
                    f"""Осталось {secs_left} секунд\n
                    {render_progressbar(parse(text), result)}"""
                    )
    bot.update_message(chat_id, message_id, update_message)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def bot_functions(bot):
    bot.reply_on_message(create_countdown)
    bot.run_bot()


def main():
    load_dotenv()

    tg_token = os.getenv('TG_TOKEN')
    bot = ptbot.Bot(tg_token)


    bot_functions(main)


if __name__ == '__main__':
    main()
