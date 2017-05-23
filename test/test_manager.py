import unittest

from controller.manager import TemplateManager, ObjectManager


class TestTemplateManager(unittest.TestCase):
    def test_load(self):
        manager = TemplateManager('../data/template', ObjectManager())

        self.assertTrue('hello_scene' in manager._scene_templates)
        print(manager._scene_templates['hello_scene'].render({'repeat': 3, 'message': 'hello?'}))


if __name__ == '__main__':
    unittest.main()
