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
            web_mods: [],
            web_list_open: false
        };
    }
6
    render() {
        return (
            <div id="page-container" className="container">
                <div className="row">
                    <div className="col">
                        <div className="btn-group installed-mods-toolbar" role="group">
                            <button
                                type="button"
                                className="btn btn-outline-success"
                                onClick={this.handleRefreshClick}>
                                Refresh
                            </button>
                            {!this.state.web_list_open && <button
                                type="button"
                                className="btn btn-outline-primary"
                                onClick={this.handleInstallMoreClick}>
                                Install more
                            </button>}
                        </div>
                    </div>

                    {this.state.web_list_open && <div className="col">
                        <div className="btn-group web-mods-toolbar" role="group">
                            <button
                                type="button"
                                className="btn btn-outline-warning"
                                onClick={this.handleCloseWebClick}>
                                Close
                            </button>
                        </div>
                    </div>}
                </div>
                <div className="row">
                    <div className="col installed-mods-col">
                        <InstalledModList mods={this.state.installed_mods} />
                    </div>
                    {this.state.web_list_open && <div className="col web-mods-col">
                        <WebModList mods={this.state.web_mods} />
                    </div>}
                </div>
            </div>
        );
    }

    componentDidMount() {
        const socket = this.context;

        socket.on('carrot', carrot => {
            this.setState({ installed_mods: carrot.mods });
        });

        this.requestGetCarrot();

        fetch('https://api.carrot-mc.xyz/prod/mods')
            .then(response => response.json())
            .then(response => this.setState({ web_mods: response.result }));
    }

    handleRefreshClick = () => {
        this.requestGetCarrot();
    };

    handleInstallMoreClick = () => {
        this.setState({ web_list_open: true })
    };

    handleCloseWebClick = () => {
        this.setState({ web_list_open: false })
    };

    requestGetCarrot() {
        const socket = this.context;
        socket.emit('get-carrot');
    }
}
