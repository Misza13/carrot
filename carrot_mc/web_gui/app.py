from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='')
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path, cache_timeout=-1)
