from argparse import Namespace

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from carrot_mc.backend import BackendService
from carrot_mc.carrot import CarrotService, InstallationManager
from carrot_mc.data import Automappable

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)


class SocketEventRouter:
    def handle(self, event: str, payload=None):
        if not payload:
            socketio.emit(event, {})

        if isinstance(payload, Namespace):
            payload = vars(payload)

        converted = dict()
        for k, v in payload.items():
            if isinstance(v, Automappable):
                converted[k] = v.to_dict()
            else:
                converted[k] = v

        socketio.emit(event, converted)


socket_router = SocketEventRouter()

backend_service = BackendService()
installation_manager = InstallationManager(backend_service, socket_router)
carrot_service = CarrotService(backend_service, installation_manager, socket_router)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path, cache_timeout=-1)


@socketio.on('install')
def handle_install(event):
    carrot_service.install(Namespace(**event, channel=None))


@socketio.on('carrot status')
def handle_carrot_status():
    carrot = carrot_service.get_status()
    socketio.emit('carrot status', carrot.to_dict())


@socketio.on('carrot enable')
def handle_carrot_enable(event):
    carrot_service.enable(Namespace(**event))


@socketio.on('carrot disable')
def handle_carrot_enable(event):
    carrot_service.disable(Namespace(**event))


def run_socket_app():
    socketio.run(app)
