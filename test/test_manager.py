import unittest
from pathlib import Path

from controller.manager import TemplateManager, ObjectManager, SignageManager
from webserver.web_server import WebServer


class TestTemplateManager(unittest.TestCase):
    def test_load(self):
        obj_mng = ObjectManager()
        tpl_mng = TemplateManager('../data/template', obj_mng)
        sgn_mng = SignageManager('../data/signage', obj_mng, tpl_mng)

        self.assertTrue('hello_scene' in tpl_mng._scene_templates)
        self.assertTrue('default_signage' in sgn_mng._signages)

        print(sgn_mng.get_signage('default_signage').render())


class TestWebServer(unittest.TestCase):
    def test_start(self):
        server = WebServer(Path('../data'))
        server.start()  # todo: causes infinite loop


if __name__ == '__main__':
    unittest.main()
