from unittest import TestCase
from bot.item import Item
from bot import base


class TestLarder(TestCase):

    def setUp(self):

        self.session = base.Session()
        base.Base.metadata.create_all(base.engine)
        brot = Item("Brot")
        self.session.add(brot)
        self.session.commit()



    def test_get_shopping_list(self):
        result = self.session.query(Item).all()
        self.session.query(Item).update().values(on_list=False)
        print(result)

    def test_add_to_shopping_list(self):
        self.fail()

    def test_delete_form_shopping_list(self):
        self.fail()

    def test__add_to_larder(self):
        self.fail()

    def test_get_larder(self):
        self.fail()
