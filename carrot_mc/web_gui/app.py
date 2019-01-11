from argparse import Namespace

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from carrot_mc.backend import BackendService
from carrot_mc.carrot import CarrotService, InstallationManager

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)


class SocketEventRouter:
    def handle(self, event: str, payload):
        socketio.emit(event, payload)


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
    socketio.emit('carrot result status', carrot.to_dict())


@socketio.on('carrot enable')
def handle_carrot_enable(event):
    carrot_service.enable(Namespace(**event))

    carrot = carrot_service.get_status()
    socketio.emit('carrot result status', carrot.to_dict())


@socketio.on('carrot disable')
def handle_carrot_enable(event):
    carrot_service.disable(Namespace(**event))

    carrot = carrot_service.get_status()
    socketio.emit('carrot result status', carrot.to_dict())


def run_socket_app():
    socketio.run(app)
