from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, KeyboardButton, Emoji
from uuid import uuid4
import logging
import sqlite3
import itertools
import math
import os
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Connect to the database
conn = sqlite3.connect('quoteDB', check_same_thread=False)
c = conn.cursor()

def category_names():
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    category_names = c.execute('SELECT Quote_Category FROM quotes1;').fetchall();

    custom_keyboard = [
        KeyboardButton(category_name) for category_name in set(category_names)
    ]
    custom_keyboard = [custom_keyboard[2*i : 2*(i+1)] for i in xrange(int(math.ceil(len(category_names)/2)))]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    return reply_markup

def author_names():
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    author_names = c.execute('SELECT Name FROM quotes1;').fetchall();

    custom_keyboard = [
        KeyboardButton(author_name) for author_name in set(author_names)
    ]
    custom_keyboard = [custom_keyboard[2*i : 2*(i+1)] for i in xrange(int(math.ceil(len(author_names)/2)))]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    return reply_markup

def get_random_quote(index):
    c.execute('SELECT Quote, Quote_Category, Name FROM quotes1 ORDER BY RANDOM() LIMIT 1;');
    data = c.fetchone()
    return data[index]

def get_quote_by_category(index, args):
    
    c.execute('SELECT Quote, Quote_Category, Name FROM quotes1 WHERE Name = "' + args + '" ORDER BY RANDOM() LIMIT 1;');
    quote = c.fetchone()
    
    try:
        return Emoji.THOUGHT_BALLOON + "\n" + quote[index] + " ~ " + quote[2]
    except TypeError:
        c.execute('SELECT Quote, Quote_Category, Name FROM quotes1 WHERE Quote_Category = "' + args + '" ORDER BY RANDOM() LIMIT 1;');
        quote = c.fetchone()

        return quote[index] + " ~ " + quote[2] + "\n" + Emoji.THOUGHT_BALLOON

# Define some command handlers
def start(bot, update):
    text = "Hello, I'm The Thinker, ...and I'm a thinker. I collect lots of great quotations from great people. If you would like to see some of them just type /category or /author"
    bot.sendMessage(update.message.chat_id, text=text)

def category(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Bleep. Bloop.",
            reply_markup=category_names())

def author(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Bleep. Bloop.",
            reply_markup=author_names())

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="@thethinkerbot finds you great quotes from great minds. /category - get quote by category\n /author - get quote by author")

def user_reply(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_quote_by_category(0, update.message.text))

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # The EventHandler
    updater = Updater(os.getenv('TOKEN'))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("category", category))
    dp.add_handler(CommandHandler("author", author))

    # On nocommand
    dp.add_handler(MessageHandler([Filters.text], user_reply))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
