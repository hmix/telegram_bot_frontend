# spec https://notes.status.im/_zy_XbciTQqQDzVrnTJ7TA?edit

import logging
from time import sleep

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

updater = Updater(token=config.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
FEEL_OK, COUGH_FEVER, STRESSED_ANXIOUS, WANNA_HELP, TELL_FRIENDS = range(5)


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


yes_no_keyboard = ReplyKeyboardMarkup([["Yes", "No"]])
yesfilter = Filters.regex('^Yes$')
nofilter = Filters.regex('^No$')


def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def areyouok(update, context):
    update.message.reply_text("Hi! Are you feeling Ok?", reply_markup=yes_no_keyboard)
    return FEEL_OK


def cough(update, context):
    update.message.reply_text("Oh no, I'm sorry about that! Are you having cough or fever?", reply_markup=yes_no_keyboard)
    return COUGH_FEVER


def stressed(update, context):
    update.message.reply_text("Good! Are you feeling stressed or anxious?", reply_markup=yes_no_keyboard)
    return STRESSED_ANXIOUS


def wannahelp(update, context):
    update.message.reply_text("That's great! Do you wanna help?", reply_markup=yes_no_keyboard)
    return WANNA_HELP


def bye(update, context):
    update.message.reply_text("Okay, Bye!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def doctorsroom(update, context):
    user = update.effective_user
    context.bot.send_message(chat_id=config.doctor_room, text="A user requested medical help: {}".format(user.first_name))
    update.message.reply_text("Forwarded your request to the doctor's room!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def psychologistsroom(update, context):
    user = update.effective_user
    context.bot.send_message(chat_id=config.psychologist_room, text="A user requested psychological help: {}".format(user.first_name))
    update.message.reply_text("Forwarded your request to the psychologists' room!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def newmembersroom(update, context):
    user = update.effective_user
    context.bot.send_message(chat_id=config.newmembers_room, text="A user wants to help: {}".format(user.first_name))
    update.message.reply_text("Forwarded your request to the new members' room!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', areyouok)],
    states={
        FEEL_OK: [MessageHandler(yesfilter, wannahelp),
                  MessageHandler(nofilter, cough)],

        WANNA_HELP: [MessageHandler(yesfilter, newmembersroom),
                     MessageHandler(nofilter, bye)],

        COUGH_FEVER: [MessageHandler(yesfilter, doctorsroom),
                      MessageHandler(nofilter, stressed)],

        STRESSED_ANXIOUS: [MessageHandler(yesfilter, psychologistsroom),
                           MessageHandler(nofilter, bye)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

start_handler = CommandHandler('start', start)
forward_to_room_handler = MessageHandler(Filters.text, forward_to_room)
response_handler = MessageHandler(Filters.text, response)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(forward_to_room_handler)
dispatcher.add_handler(response_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
