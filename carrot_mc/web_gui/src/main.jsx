import React from 'react';
import ReactDOM from 'react-dom';
import io from 'socket.io-client';

import 'bootstrap';
import './main.css';

import CarrotApp from './app.jsx';

import SocketContext from './socket.context.jsx';

const socket = io('http://localhost:5000/');

ReactDOM.render(
    <SocketContext.Provider value={socket}>
        <CarrotApp />
    </SocketContext.Provider>,
    document.getElementById('root')
);