import unittest

from controller.manager import TemplateManager, ObjectManager


class TestTemplateManager(unittest.TestCase):
    def test_load(self):
        manager = TemplateManager('../data/template', ObjectManager())

        self.assertTrue('empty_scene' in manager._scene_templates)


if __name__ == '__main__':
    unittest.main()
