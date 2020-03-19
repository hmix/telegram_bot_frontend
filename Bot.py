# spec https://notes.status.im/_zy_XbciTQqQDzVrnTJ7TA?edit


import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
Token = ''
bot = telegram.Bot(token=Token)
updater = Updater(token=Token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="First: add your telegram "
                                                                    "account. Don't forget the @ !"

                                                                    "Please describe your "
                                                                    "current situation briefly. "
                                                                    "Don't forget to mention "
                                                                    "things like your body "
                                                                    "temperature.")


def forward_to_room(update, context):
    sleep(15)
    context.bot.send_message(chat_id='@humanbios0k', text=update.message.text)


def response(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You're information is "
                                                                    "being processed. A care "
                                                                    "taker will send you a "
                                                                    "message with further "
                                                                    "instructions immediately. "
                                                                    "Please be patient and "
                                                                    "sorry for letting you wait")

    # keep patient buisy and calm them down, for more instructions
    # Keep asking questions, try calming the patient down, while gathering more information for
    # more information see https://humanbios.org/more


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Okay that helps, thank you "
                                                                    "can you tell me more about "
                                                                    "your situation?")


start_handler = CommandHandler('start', start)
forward_to_room_handler = MessageHandler(Filters.text, forward_to_room)
response_handler = MessageHandler(Filters.text, response)
echo_handler = MessageHandler(Filters.text, echo)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(forward_to_room_handler)
dispatcher.add_handler(response_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
