import threading

import flask
import flask_socketio

from controller.manager import ObjectManager, TemplateManager, SignageManager


class WebServer:
    def __init__(self, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        self._flask_server = FlaskServer(obj_mng, tpl_mng, sgn_mng)
        self._flask_io_server = FlaskIOServer(sgn_mng)

    def start(self):
        self._flask_server.start()
        self._flask_io_server.start()


class FlaskServer(threading.Thread):
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

        super().__init__()

    def run(self):
        self._app.run()

    def handle_signage_list(self) -> str:
        return ' '.join(['<a href="/{0}">{0}</a>'.format(str(x)) for x in self._sgn_mng.signages.keys()])

    def handle_signage(self, signage_id: str) -> str:
        return self._sgn_mng.get_signage(signage_id).render()

    def handle_template_static(self, path: str) -> str:
        return self._app.send_static_file(path)


class FlaskIOServer(threading.Thread):
    def __init__(self, sgn_mng: SignageManager):
        self._sgn_mng = sgn_mng
        self._app = flask.Flask(__name__)
        self._socket_io = flask_socketio.SocketIO(self._app)

        super().__init__()

    def run(self):
        self._socket_io.run(self._app, port=5100)


class Client:
    pass


class Scheduler:
    pass
