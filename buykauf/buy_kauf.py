import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import Config
from bot.buy_kauf_bot import BuyKaufBot


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    logger = logging.getLogger("minna.start")
    logger.info("start")
    update.message.reply_text(
        'Hi! Ich bin der Bot:)')


def help(update, context):
    message = "Hallo ich bin der BuyKaufBot und habe folgende Befehle:\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message)


def main():
    logger = logging.getLogger("BuyKauf")
    logger.info("started BuyKaufBot")
    conf = Config()
    bbot = BuyKaufBot()

    TOKEN = conf['TOKEN']

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", bbot.get_list_dialog))
    dp.add_handler(CommandHandler("reset", bbot.reset_shopping_list))
    dp.add_handler(CommandHandler("add", bbot.add_item_from_items_dialog))
    dp.add_handler(CommandHandler("del", bbot.delete_from_larder_dialog))
    dp.add_handler(CallbackQueryHandler(bbot.main_handler_button))
    dp.add_handler(MessageHandler(Filters.regex('^\+'), bbot.add_item))

    dp.add_error_handler(bbot.error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
