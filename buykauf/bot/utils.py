import functools
import json
from contextlib import contextmanager
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from .base import Session


def send(func):
    @functools.wraps(func)
    def wrapper_send(*args, **kwargs):
        message = func(*args, **kwargs)
        args[2].bot.send_message(
            chat_id=args[1].effective_chat.id,
            text=message)
        return message

    return wrapper_send


def send_inline_keyboard(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper_inline(*args, **kwargs):
            keyboard = func(*args, **kwargs)
            assert type(keyboard) == list
            reply_markup = InlineKeyboardMarkup(keyboard)
            args[2].bot.send_message(chat_id=args[1].message.chat_id, text=text, reply_markup=reply_markup)
            return keyboard
        return wrapper_inline
    return decorator


def build_menu(buttons,
               n_cols,
               button_type,
               header_buttons=None,
               footer_buttons=None):
    buttons = [InlineKeyboardButton(button,
                    callback_data=json.dumps({'name': button, 'type': button_type})) for button in buttons]
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @functools.wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator




@contextmanager
def session_scope(tele_error):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        tele_error.message += "\n" + str(e)
        raise tele_error
    finally:
        session.close()
