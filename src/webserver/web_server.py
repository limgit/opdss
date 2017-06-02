import flask

from controller.manager import ObjectManager, TemplateManager, SignageManager


class WebServer:
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        self._app = flask.Flask(__name__)
        self._app.static_folder = str(tpl_mng._dir_root.resolve())
        self._app.add_url_rule('/favicon.ico', 'favicon', lambda: '')
        self._app.add_url_rule('/', 'handle_signage_list', self.handle_signage_list)
        self._app.add_url_rule('/<signage_id>', 'handle_signage', self.handle_signage)
        self._app.add_url_rule('/_/<path:path>', 'handle_template_static', self.handle_template_static)

        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

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
