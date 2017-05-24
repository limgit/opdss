import unittest

from controller.manager import TemplateManager, ObjectManager, SignageManager


class TestTemplateManager(unittest.TestCase):
    def test_load(self):
        obj_mng = ObjectManager()
        tpl_mng = TemplateManager('../data/template', obj_mng)
        sgn_mng = SignageManager('../data/signage', obj_mng, tpl_mng)

        self.assertTrue('hello_scene' in tpl_mng._scene_templates)
        self.assertTrue('default_signage' in sgn_mng._signages)

        print(sgn_mng.get_signage('default_signage').render())


if __name__ == '__main__':
    unittest.main()
