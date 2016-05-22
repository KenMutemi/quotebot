from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, sqlite3

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Connect to and query the sqlite database
conn = sqlite3.connect('quoteDB')
c = conn.cursor()
c.execute('SELECT Quote, Quote_Category, Name FROM quotes1 ORDER BY RANDOM() LIMIT 1;');
data = c.fetchone()

# Define some command handlers
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="%s" % data[0])

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

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

    # on nocommand
    dp.add_handler(MessageHandler([Filters.text], echo))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
