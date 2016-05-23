from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup, KeyboardButton, Emoji
from uuid import uuid4
import logging, sqlite3, re

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
    custom_keyboard = [[
        KeyboardButton(category_name) for category_name in category_names
        ]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    return reply_markup

def get_random_quote(index):
    c.execute('SELECT Quote, Quote_Category, Name FROM quotes1 ORDER BY RANDOM() LIMIT 1;');
    data = c.fetchone()
    return data[index]

def get_quote_by_category(index, args):
    category = ''.join(args)
    c.execute('SELECT Quote, Quote_Category, Name FROM quotes1 WHERE Quote_Category = "' + category.title() + '" ORDER BY RANDOM() LIMIT 1;');
    data = c.fetchone()
    return data[index]

# Define some command handlers
def start(bot, update):
    text = "My name is The Thinker, and I'm a genius. I collect lots of great quotations from great people like me. If you would like to see some of them just type /category [category] and I will produce a random quote from my stash of wisdom." + category_names()
    bot.sendMessage(update.message.chat_id, text=text)

def category(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Meow. Here's a list of the quote categories I have.",
            reply_markup=category_names())

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def user_reply(bot, update):
    bot.sendMessage(update.message.chat_id, text=get_quote_by_category(0, update.message.text))

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # The EventHandler
    updater = Updater("227558452:AAG3aRfAMhBcQ8dvUymJ1rXVBA5BnjoPlZQ")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on command
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("category", category))

    # On nocommand
    dp.add_handler(MessageHandler([Filters.text], user_reply))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
