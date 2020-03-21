#!/usr/bin/env python3
# coding: utf-8

"""
telegram bot to connect corona-suspects with medical staff 

Bot url:
t.me/corona_care_bot


groups the bot forwards to: (has to be a member of the group)
https://t.me/humanbios0k

"""

import os
import json
import dotenv
import requests
import telegram
import time
import textwrap

import logging

from pathlib import Path
from telegram.ext import Updater, CommandHandler, CallbackContext

# enable logging
logging.basicConfig(
    format='{asctime} {name} {levelname} {message}',
    style='{',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

# load bot token from .env
env_path = Path('.') / '.env'
dotenv.load_dotenv(env_path)
TELEGRAM_BOT_CORONA_TOKEN = os.getenv("TELEGRAM_BOT_CORONA_TOKEN")

# the bot's URL
URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_CORONA_TOKEN}"


# commands
def start(update: telegram.Update, context: CallbackContext):
    """sent when the bot is talked to"""
    # Stuff here
    # args will be available as context.args
    # jobqueue will be available as context.jobqueue

    WELCOME_MESSAGE = """
        First: add your telegram
        account. Don't forget the @ !
        Please describe your
        current situation briefly.
        Don't forget to mention
        things like your body
        temperature.
        """

    context.bot.send_message(chat_id=update.effective_chat.id, text=textwrap.dedent(WELCOME_MESSAGE))


# helper methods
def forward_to_room(update, context):
    context.bot.send_message(chat_id='@humanbios0k', text=update.message.text)

# TODO:
# def error_callback(update, context):
#     logger.warning(f'Update "{update}" caused error "{context.error}"')

# def job_callback(context):
#     job = context.job
#     context.bot.send_message(SOMEONE, job.context)



# main loop
def main():
    
    bot = telegram.Bot(token=TELEGRAM_BOT_CORONA_TOKEN)

    print(f'>>> DEBUG: {bot.get_me()}')
    print(f'>>> DEBUG: {bot.get_updates()}')
    logger.info('logging functional')
    
    updater = Updater(TELEGRAM_BOT_CORONA_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start',start))

    # TODO: message_handler -> FilterClass ->

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# TODO: translation api returns -> None MEDIC CARE
