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


dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
