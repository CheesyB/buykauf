import logging

from sqlalchemy.exc import IntegrityError
from telegram import InlineKeyboardMarkup, ChatAction
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from .utils import send, send_inline_keyboard, build_menu, session_scope
from .base import Base, Session, engine
from .item import Item


STRIKE = '\u0336'

class BuyKaufBot():

    def __init__(self):
        self.logger = logging.getLogger("BuyKauf")
        Base.metadata.create_all(engine)


    @send_inline_keyboard
    def get_list_dialog(self, update, context):
        with session_scope(TelegramError("hups! Die Liste konnte ich nicht kriegen...")) as session:
            items = [str(it) for it in session.query(Item).filter(Item.on_list == True)]
        return build_menu(items, 2)

    def remove_from_shopping_list_button(self, update, context):
        query = update.callback_query
        query.answer()
        with session_scope(TelegramError("Grmph!! Das konnte ich nicht löschen!")) as session:
            item = session.query(Item).filter(Item.name == update.callback_query.data).first()
            item.on_list = False
            remaining_items = [str(it) for it in session.query(Item).filter(Item.on_list == True)]
            context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                             message_id=update.callback_query.message.message_id,
                                             reply_markup=InlineKeyboardMarkup(build_menu(remaining_items, 2)))

    @send
    def reset_shopping_list(self, update, context):
        with session_scope(TelegramError("Konnte die shopping list nicht zurücksetzen:(")) as session:
            for item in session.query(Item):
                item.on_list = False
        return "keine Sachen mehr auf der Einkaufsliste"

    @send
    def add_item(self, update, context):
        args = update.message.text.split(' ')
        if len(args) <= 1:
            raise TelegramError("Ich konnte nichts hinzufügen")
        added_items = []
        with session_scope(TelegramError("Hups, keine Items hinzugefügt:")) as session:
            for item in args[1:]:
                item = self._get_or_increase_item(session, item, added_items)
                session.add(item)

        return f"Added {added_items} to shopping list"


    def add_item_from_larder(self):
        return

    def _get_or_increase_item(self, session, name, items_list):
        item = session.query(Item).filter_by(name=name).first()
        if not item:
            item = Item(name)
            items_list.append(item.name)
        else:
            item.total_count += 1
            item.on_list = True
            items_list.append(STRIKE.join(item.name) + STRIKE)
        return item

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
