import unittest
from pathlib import Path

from controller.manager import ObjectManager
from webserver.web_server import WebServer


class TestObjectManager(unittest.TestCase):
    def test_object_change(self):
        obj_mng = ObjectManager(Path('../data/data'))

        menu_item_type = obj_mng.get_object_type('menu_item')
        milk_object = obj_mng.get_object_value(menu_item_type, 'milk')
        milk_object.id = 'test'
        milk_object.id = 'milk'

        milk_object.set_value('price', 599)
        milk_object.set_value('price', 299)


class TestWebServer(unittest.TestCase):
    def test_start(self):
        server = WebServer(Path('../data'))
        server.start()  # todo: causes infinite loop


if __name__ == '__main__':
    unittest.main()
