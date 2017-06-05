import sys

import unittest
from pathlib import Path

from controller.manager import ObjectManager, TemplateManager, SignageManager, ChannelManager
from webserver.web_server import WebServer

sys.path.append("../src")
root_path = Path('../data')


class TestChannelManager(unittest.TestCase):
    def test_channel_manager(self):
        obj_mng = ObjectManager(root_path / 'data')
        tpl_mng = TemplateManager(root_path / 'template', obj_mng)
        sgn_mng = SignageManager(root_path / 'signage', obj_mng, tpl_mng)
        chn_mng = ChannelManager(root_path / 'channel', sgn_mng)

        channel = chn_mng.get_channel('default_channel')
        channel.id = 'test'
        channel.id = 'default_channel'


class TestObjectManager(unittest.TestCase):
    def test_object_change(self):
        obj_mng = ObjectManager(root_path / 'data')

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


class TestSignageManager(unittest.TestCase):
    def test_signage_change(self):
        obj_mng = ObjectManager(root_path / 'data')
        tpl_mng = TemplateManager(root_path / 'template', obj_mng)
        sgn_mng = SignageManager(root_path / 'signage', obj_mng, tpl_mng)
        default_signage = sgn_mng.get_signage('default_signage')

        # change signage's property
        default_signage.title = 'test'
        default_signage.title = 'Default Signage'

        # change scene's property
        default_signage.scenes[1].duration = 100
        default_signage.scenes[1].duration = 1

        # change reference value of a scene
        default_signage.scenes[0].values.set_value('menu_group', 'drinks')


class TestWebServer(unittest.TestCase):
    def test_start(self):
        obj_mng = ObjectManager(root_path / 'data')
        tpl_mng = TemplateManager(root_path / 'template', obj_mng)
        sgn_mng = SignageManager(root_path / 'signage', obj_mng, tpl_mng)
        server = WebServer(obj_mng, tpl_mng, sgn_mng)
        server.start()  # todo: causes infinite loop


if __name__ == '__main__':
    unittest.main()
