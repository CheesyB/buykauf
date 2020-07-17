import logging
import json
from sqlalchemy import asc
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

    @send_inline_keyboard("Einkaufsliste")
    def get_list_dialog(self, update, context):
        with session_scope(TelegramError("hups! Die Liste konnte ich nicht kriegen...")) as session:
            items = [str(it) for it in session.query(Item).filter(Item.on_list == True)]
        return build_menu(items, 2, 'rmList')

    def get_list_button(self, update, context, callback_dict):
        with session_scope(TelegramError("Grmph!! Das konnte ich nicht löschen!")) as session:
            item = session.query(Item).filter(Item.name == callback_dict['name']).first()
            item.on_list = False
            remaining_items = [str(it) for it in session.query(Item).filter(Item.on_list == True)]
            context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                                  message_id=update.callback_query.message.message_id,
                                                  reply_markup=InlineKeyboardMarkup(
                                                      build_menu(remaining_items, 2, 'rmList')))

    @send_inline_keyboard("Vorratskammer")
    def add_item_from_items_dialog(self, update, context):
        with session_scope(TelegramError("Kann keine Liste erstellen.")) as session:
            items = [str(it) for it in session.query(Item).filter(Item.on_list == False).order_by(asc(Item.name))]
        return build_menu(items, 2, 'add')

    def add_item_from_items_button(self, update, context, callback_dict):
        with session_scope(TelegramError("Kann keine Liste erstellen.")) as session:
            item = session.query(Item).filter(Item.name == callback_dict['name']).first()
            item.on_list = True
            items = [str(it) for it in session.query(Item).filter(Item.on_list == False).order_by(Item.total_count)]
            context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                                  message_id=update.callback_query.message.message_id,
                                                  reply_markup=InlineKeyboardMarkup(build_menu(items, 2, 'add')))

    @send_inline_keyboard("Löschen aus Vorratskammer")
    def delete_from_larder_dialog(self, update, context):
        with session_scope(TelegramError("Kann leider nicht aus der Vorratskammer löschen.")) as session:
            items = [str(it) for it in session.query(Item).order_by(Item.total_count)]
        return build_menu(items, 2, 'rmLarder')

    def delete_from_larder_button(self, update, context, callback_dict):
        with session_scope(TelegramError("Dieses Element konnte ich leider nicht löschen")) as session:
            session.query(Item).filter(Item.name == callback_dict['name']).delete()
            items = [str(it) for it in session.query(Item).all()]
            context.bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                                  message_id=update.callback_query.message.message_id,
                                                  reply_markup=InlineKeyboardMarkup(
                                                      build_menu(items, 2, 'rmLarder')))

    def main_handler_button(self, update, context):
        query = update.callback_query
        query.answer()
        callback_dict = json.loads(update.callback_query.data)
        if callback_dict['type'] == 'rmList':
            self.get_list_button(update, context, callback_dict)
        if callback_dict['type'] == 'add':
            self.add_item_from_items_button(update, context, callback_dict)
        if callback_dict['type'] == 'rmLarder':
            self.delete_from_larder_button(update, context, callback_dict)


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


