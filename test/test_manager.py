import sys
sys.path.append("../src")

import unittest
from pathlib import Path

from controller.manager import ObjectManager, TemplateManager, SignageManager
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

        menu_group_type = obj_mng.get_object_type('menu_group')
        drinks_object = obj_mng.get_object_value(menu_group_type, 'drinks')
        drinks_object.set_value('name', 'test')
        drinks_object.set_value('name', 'Drinks')


class TestWebServer(unittest.TestCase):
    def test_start(self):
        root_path = Path('../data')

        obj_mng = ObjectManager(root_path / 'data')
        tpl_mng = TemplateManager(root_path / 'template', obj_mng)
        sgn_mng = SignageManager(root_path / 'signage', obj_mng, tpl_mng)

        server = WebServer(obj_mng, tpl_mng, sgn_mng)
        server.start()  # todo: causes infinite loop


if __name__ == '__main__':
    unittest.main()
