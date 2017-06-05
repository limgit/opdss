import threading

import flask
import flask_socketio

from controller.manager import ObjectManager, TemplateManager, SignageManager, ChannelManager


class WebServer:
    def __init__(self, chn_mng: ChannelManager, obj_mng: ObjectManager, tpl_mng: TemplateManager, sgn_mng: SignageManager):
        self._app = flask.Flask(__name__)
        self._app.static_folder = str(tpl_mng._dir_root.resolve())
        self._app.add_url_rule('/favicon.ico', 'favicon', lambda: '')
        self._app.add_url_rule('/', 'handle_channel_list', self.handle_channel_list)
        self._app.add_url_rule('/<channel_id>', 'handle_channel', self.handle_channel)
        self._app.add_url_rule('/_/<path:path>', 'handle_template_static', self.handle_template_static)

        self._chn_mng = chn_mng
        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng

        self._socket_io = flask_socketio.SocketIO(self._app)
        self._io_server = FlaskIOServer()

        self._socket_io.on_namespace(self._io_server)

        super().__init__()

    def start(self):
        threading.Thread(target=self._app.run).start()
        threading.Thread(target=self._socket_io.run, args=(self._app, None, 5100)).start()

    def handle_channel_list(self) -> str:
        return ' '.join(['<a href="/{0}">{0}</a>'.format(str(x)) for x in self._chn_mng.channels.keys()])

    def handle_channel(self, channel_id: str) -> str:
        return self._chn_mng.get_channel(channel_id).signage.render()

    def handle_template_static(self, path: str) -> str:
        return self._app.send_static_file(path)


class FlaskIOServer(flask_socketio.Namespace):
    def on_connect(self):
        return True


class Client:
    pass


class Scheduler:
    pass
