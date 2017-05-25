from pathlib import Path

import flask
from flask import app

from controller.manager import ObjectManager, TemplateManager, SignageManager


class WebServer:
    def __init__(self, root_path: Path):
        self._root_path = root_path.resolve()

        self._app = flask.Flask(__name__)
        self._app.static_folder = str(self._root_path) + '/template/scene/'
        self._app.add_url_rule('/', 'handle_signage_list', self.handle_signage_list)
        self._app.add_url_rule('/<signage_id>', 'handle_signage', self.handle_signage)
        self._app.add_url_rule('/_/<path:path>', 'handle_template_static', self.handle_template_static)

        self._obj_mng = ObjectManager()
        self._tpl_mng = TemplateManager(str(self._root_path) + '/template', self._obj_mng)
        self._sgn_mng = SignageManager(str(self._root_path) + '/signage', self._obj_mng, self._tpl_mng)

    def start(self):
        self._app.run()

    def handle_signage_list(self) -> str:
        return ' '.join(['<a href="/{0}">{0}</a>'.format(str(x)) for x in self._sgn_mng._signages.keys()])

    def handle_signage(self, signage_id: str) -> str:
        return self._sgn_mng.get_signage(signage_id).render()

    def handle_template_static(self, path: str) -> str:
        return self._app.send_static_file(path)


class Client:
    pass


class Scheduler:
    pass
