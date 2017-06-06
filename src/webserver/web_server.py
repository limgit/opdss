import threading

import flask
import flask_socketio

from controller.manager import ObjectManager, TemplateManager, SignageManager, ChannelManager, MultimediaManager
from model.channel import Channel


class WebServer:
    def __init__(self, chn_mng: ChannelManager, obj_mng: ObjectManager, tpl_mng: TemplateManager,
                 sgn_mng: SignageManager, mtm_mng: MultimediaManager):
        self._app = flask.Flask(__name__)
        self._app.static_folder = str(tpl_mng.root_dir.resolve())
        self._app.add_url_rule('/favicon.ico', 'favicon', lambda: '')
        self._app.add_url_rule('/', 'handle_channel_list', self.handle_channel_list)
        self._app.add_url_rule('/<channel_id>', 'handle_channel', self.handle_channel)
        self._app.add_url_rule('/_/image/<file_name>', 'handle_image_static', self.handle_image_static)
        self._app.add_url_rule('/_/video/<file_name>', 'handle_video_static', self.handle_video_static)
        self._app.add_url_rule('/_/<path:path>', 'handle_template_static', self.handle_template_static)

        self._chn_mng = chn_mng
        self._obj_mng = obj_mng
        self._tpl_mng = tpl_mng
        self._sgn_mng = sgn_mng
        self._mtm_mng = mtm_mng

        self._socket_io = flask_socketio.SocketIO(self._app, ping_interval=10, ping_timeout=60)
        self._io_server = FlaskIOServer(self._socket_io)

        def redirect_event(channel: Channel, old_id: str):
            self._io_server.request_redirect(old_id, channel.id)

        def count_event(channel: Channel):
            return self._io_server.get_connections(channel.id)

        self._chn_mng.redirect_event_handler = redirect_event
        self._chn_mng.count_event_handler = count_event

        self._socket_io.on_namespace(self._io_server)

        super().__init__()

    def start(self):
        threading.Thread(target=lambda: self._socket_io.run(self._app)).start()

    def stop(self):
        self._socket_io.stop()

    def handle_channel_list(self) -> str:
        return ' '.join(['<a href="/{0}">{0}</a>'.format(str(x)) for x in self._chn_mng.channels.keys()])

    def handle_channel(self, channel_id: str) -> str:
        return self._chn_mng.get_channel(channel_id).signage.render(self._sgn_mng.root_dir)

    def handle_template_static(self, path: str) -> str:
        return self._app.send_static_file(path)

    def handle_image_static(self, file_name: str) -> int:
        print(self._mtm_mng.image_type.root_dir, file_name)
        return flask.send_from_directory(self._mtm_mng.image_type.root_dir, file_name)

    def handle_video_static(self, file_name: str) -> int:
        return flask.send_from_directory(self._mtm_mng.video_type.root_dir, file_name)


class FlaskIOServer(flask_socketio.Namespace):
    def __init__(self, socket_io):
        super().__init__()
        self._socket_io = socket_io
        self._connections = dict()

    def on_connect(self):
        return True

    def on_disconnect(self):
        for room in flask_socketio.rooms():
            if room not in self._connections.keys():
                continue

            self._connections[room] -= 1

    def on_enter(self, data: dict):
        room_name = data['room']
        flask_socketio.join_room(room_name)

        if room_name not in self._connections.keys():
            self._connections[room_name] = 0

        self._connections[room_name] += 1

    def request_redirect(self, from_channel: str, to_channel: str):
        self._socket_io.emit('redirect', {'to': to_channel}, room=from_channel, broadcast=True)

    def get_connections(self, room_id: str):
        if room_id not in self._connections.keys():
            return 0

        return self._connections[room_id]
