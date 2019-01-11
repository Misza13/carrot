from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from carrot_mc.backend import BackendService
from carrot_mc.carrot import CarrotService, InstallationManager

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)

backend_service = BackendService()
installation_manager = InstallationManager(backend_service)
carrot_service = CarrotService(backend_service, installation_manager)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path, cache_timeout=-1)


@socketio.on('install')
def handle_install(event):
    class InstallRequest:
        def __init__(self, event):
            self.mod_key = [event['mod_key']]
            self.channel = None

    carrot_service.install(InstallRequest(event))


@socketio.on('carrot status')
def handle_carrot_status():
    carrot = carrot_service.get_status()
    socketio.emit('carrot result status', carrot.to_dict())


@socketio.on('carrot enable')
def handle_carrot_enable(event):
    class EnableRequest:
        def __init__(self, event):
            self.mod_key = [event['mod_key']]

    carrot_service.enable(EnableRequest(event))

    carrot = carrot_service.get_status()
    socketio.emit('carrot result status', carrot.to_dict())


@socketio.on('carrot disable')
def handle_carrot_enable(event):
    class DisableRequest:
        def __init__(self, event):
            self.mod_key = [event['mod_key']]

    carrot_service.disable(DisableRequest(event))

    carrot = carrot_service.get_status()
    socketio.emit('carrot result status', carrot.to_dict())


def run_socket_app():
    socketio.run(app)
