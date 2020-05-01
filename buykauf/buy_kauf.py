import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import Config
from bot.buy_kauf_bot import BuyKaufBot




def help(update, context):
    message = "Hallo ich bin die Minna. Ich habe eine Vorratskammer und eine Einkaufsliste. Alles was auf" \
              "der Einkaufliste steht ist auch gleichzeitig in der Vorratskammer. Um eine neues Einkaufsding" \
              "hinzuzufügen einfach:\n"\
              "+ und alles was hinzu kommen soll mit Leerzeichen\n" \
              "das fügt dann die Sachen in die Vorratskammer aber auch auf die Einkaufsliste. Die kannst du mit:" \
              "/list abrufen" \
              "Wenn du hier auf eine Button drücks verschwindet es von der List und ist somit wahrscheinlich gekauft.\n" \
              "/add fügt von der Vorratskammer in die Einkaufsliste und\n" \
              "/reset löscht die Einkaufsliste mit\n" \
              "/del löscht du Items aus der Vorratskammer (vorsicht:) sonst ist alles weg..."
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
    dp.add_handler(CommandHandler("help", help))
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
