import React from 'react';

import './app.css';

import WebModList from './web.mod.list';
import SocketContext from "./socket.context";
import InstalledModList from "./installed.mod.list";

export default class CarrotApp extends React.Component {
    static contextType = SocketContext;

    constructor(props) {
        super(props);

        this.state = {
            installed_mods: [],
            web_mods: []
        };
    }

    render() {
        return (
            <div id="page-container" className="container">
                <div className="row">
                    <div className="col-5 installed-mods-col">
                        <InstalledModList mods={this.state.installed_mods} />
                    </div>
                    <div className="col-7 web-mods-col">
                        <WebModList mods={this.state.web_mods} />
                    </div>
                </div>
            </div>
        );
    }

    componentDidMount() {
        const socket = this.context;

        socket.on('carrot', carrot => {
            this.setState({ installed_mods: carrot.mods });
        });

        socket.emit('get-carrot');

        fetch('https://api.carrot-mc.xyz/prod/mods')
            .then(response => response.json())
            .then(response => this.setState({ web_mods: response.result }));
    }
}
