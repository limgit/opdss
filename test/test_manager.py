import sys

import unittest
from pathlib import Path

from controller.manager import ObjectManager, TemplateManager, SignageManager, ChannelManager, MultimediaManager
from webserver.web_server import WebServer

sys.path.append("../src")
root_path = Path('../data')


class TestChannelManager(unittest.TestCase):
    def test_channel_manager(self):
        mtm_mng = MultimediaManager(root_path / 'media')
        obj_mng = ObjectManager(root_path / 'data', mtm_mng)
        tpl_mng = TemplateManager(root_path / 'template', obj_mng)
        sgn_mng = SignageManager(root_path / 'signage', obj_mng, tpl_mng)
        chn_mng = ChannelManager(root_path / 'channel', sgn_mng)

        channel = chn_mng.get_channel('default_channel')
        channel.id = 'test'
        channel.id = 'default_channel'


class TestObjectManager(unittest.TestCase):
    def test_object_change(self):
        mtm_mng = MultimediaManager(root_path / 'media')
        obj_mng = ObjectManager(root_path / 'data', mtm_mng)

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
        mtm_mng = MultimediaManager(root_path / 'media')
        obj_mng = ObjectManager(root_path / 'data', mtm_mng)
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
        mtm_mng = MultimediaManager(root_path / 'media')
        obj_mng = ObjectManager(root_path / 'data', mtm_mng)
        tpl_mng = TemplateManager(root_path / 'template', obj_mng)
        sgn_mng = SignageManager(root_path / 'signage', obj_mng, tpl_mng)
        chn_mng = ChannelManager(root_path / 'channel', sgn_mng)

        server = WebServer(chn_mng, obj_mng, tpl_mng, sgn_mng, mtm_mng)
        server.start()  # todo: causes infinite loop


class TestMultimedia(unittest.TestCase):
    def test_file_change(self):
        multi_mng = MultimediaManager(root_path / 'media')
        image_path = root_path / 'multimedia' / 'image'
        video_path = root_path / 'multimedia' / 'video'

        #multi_mng.add_image(Path('C:/Users/sumin/PycharmProjects/guess/data/multimedia/image/1.jpg'))
        multi_mng.add_image(image_path / '1.jpg')
        multi_mng.get_images('1.jpg').file_name = 'test.jpg'
        multi_mng.add_image(image_path / 'test.jpg')
        multi_mng.get_images('test.jpg').file_name = '1.jpg'

        multi_mng.add_video(video_path / '2.MOV')
        multi_mng.get_videos('2.MOV').file_name = 'test.MOV'
        multi_mng.add_video(video_path / 'test.MOV')
        multi_mng.get_videos('test.MOV').file_name = '2.MOV'


if __name__ == '__main__':
    unittest.main()
