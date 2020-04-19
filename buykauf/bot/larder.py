import logging
import time
import dataset
from telegram import TelegramError


class Larder():

    def __init__(self, connection):
        self.logger = logging.getLogger('Larder')
        self.db = dataset.connect(f'sqlite:///:memory:')
        self.logger.info("DB connection established")
        self.db.get_table("shopping_list")
        self.db.get_table("larder")

    def get_shopping_list(self):
        return self.db['shopping_list']

    def add_to_shopping_list(self, items):
        for item in items:
            self._add_to_larder(item)
            result = self.db['shopping_list'].upsert(dict(name=item), ['name'])
            if not result:
                raise TelegramError("Hups, das war schon auf der Liste")

    def delete_form_shopping_list(self, item):
        try:
            self.db['shopping_list'].delete(name=item)
        except Exception:
            raise TelegramError(f"Diese Item war nicht in der Liste: {item}")

    def _add_to_larder(self, item):
        result = self.db['larder'].insert_ignore(dict(name=item, _count=1), ['name'])
        if not result:
            result = self.db['larder'].find_one(name=item)
            result['_count'] += 1
            self.db['larder'].update(result, ['name'])

    def get_larder(self):
        return self.db['larder']

