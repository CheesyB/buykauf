import logging

import dataset
from telegram import InlineKeyboardMarkup, ChatAction
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from .utils import send, send_inline_keyboard, build_menu, send_action
from .larder import Larder


class BuyKaufBot():

    def __init__(self, connection):
        self.logger = logging.getLogger("BuyKauf")
        self.larder = Larder(connection)

    @send_inline_keyboard
    def get_list_dialog(self, update, context):
        return build_menu(LIST, 2)

    def button(self, update, context):
        query = update.callback_query

        query.answer()
        reply_markup = update.effective_message['reply_markup']
        LIST.remove(query.data)
        context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                             message_id=update.callback_query.message.message_id,
                                             reply_markup=InlineKeyboardMarkup(build_menu(LIST, 2)))
        
    @send
    def add_item(self, update, context):
        args = update.message.text.split(' ')
        self.larder.add_to_shopping_list(args[1:])
        return f"Added {args[1:]} to shopping list"

    def add_item_from_larder(self):
        return

    @send_inline_keyboard
    def add_from_list(self):
        return build_menu(LARDER, 2)


    @send
    def error_callback(self, update, context):
        logger = logging.getLogger("BuyKauf.error")
        try:
            raise context.error
        except Unauthorized as e:
            logger.warning(e)
            return "Unauthorized - " + str(e)

        except BadRequest as e:
            logger.warning(e)
            return "BadRequest - " + str(e)

        except TimedOut as e:
            logger.warning(e)
            return "TimedOut - " + str(e)

        except NetworkError as e:
            logger.warning(e)
            return "NetworkError - " + str(e)

        except ChatMigrated as e:
            logger.warning(e)
            return "ChatMigrated - " + str(e)

        except TelegramError as e:
            logger.warning(e)
            return "TeleError - " + str(e)
