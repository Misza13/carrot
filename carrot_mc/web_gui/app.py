from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from carrot_mc.carrot import CarrotService

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)

carrot_service = CarrotService()


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


def run_socket_app():
    socketio.run(app)