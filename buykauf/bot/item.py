import logging

from sqlalchemy import Column, UniqueConstraint
from telegram import TelegramError
from sqlalchemy import Integer, String, Boolean
from .base import Base


class Item(Base):

    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(32))
    on_list = Column('on_list', Boolean)
    quantity = Column('quantity', Integer)
    total_count = Column('total_count', Integer)
    __table_args__ = (UniqueConstraint('name'),)

    def __init__(self, name, on_list=True, quantity=1):
        self.name = name
        self.on_list = on_list
        self.quantity = quantity
        self.total_count = 1

    def __str__(self):
        return self.name

    # def get_shopping_list(self):
    #     return self.db['shopping_list']
    #
    # def add_to_shopping_list(self, items):
    #     for item in items:
    #         self._add_to_items(item)
    #         result = self.db['shopping_list'].upsert(dict(name=item), ['name'])
    #         if not result:
    #             raise TelegramError('Hups, das war schon auf der Liste')
    #
    # def delete_form_shopping_list(self, item):
    #     try:
    #         self.db['shopping_list'].delete(name=item)
    #     except Exception:
    #         raise TelegramError(f'Diese Item war nicht in der Liste: item')
    #
    # def _add_to_items(self, item):
    #     result = self.db['items'].insert_ignore(dict(name=item, _count=1), ['name'])
    #     if not result:
    #         result = self.db['items'].find_one(name=item)
    #         result['_count'] += 1
    #         self.db['items'].update(result, ['name'])
    #
    # def get_items(self):
    #     return self.db['items']



