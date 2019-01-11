import React from 'react';

import InstalledModItem from "./installed.mod.item";

import './installed.mod.list.css';
import SocketContext from "./socket.context";

export default class InstalledModList extends React.Component {
    static contextType = SocketContext;

    constructor(props) {
        super(props);

        this.state = {
            mods: []
        };
    }

    render() {
        return (
            <div className="container mod-list">
                <div className="row">
                    <div className="col">
                        <div className="btn-group installed-mods-toolbar" role="group">
                            <button
                                type="button"
                                className="btn btn-outline-success"
                                onClick={this.handleRefreshClick}>
                                Refresh
                            </button>
                            {!this.props.webListOpen && <button
                                type="button"
                                className="btn btn-outline-primary"
                                onClick={this.handleInstallMoreClick}>
                                Install more
                            </button>}
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col installed-mods-col">
                        {this.state.mods.map(mod => <InstalledModItem key={mod.key} mod={mod} />)}
                    </div>
                </div>
            </div>
        );
    }

    componentDidMount() {
        const socket = this.context;

        socket.on('carrot status', carrot_status => {
            this.setState({ mods: carrot_status.mods });
        });

        socket.on('mod_enabled', () => {
            this.requestGetCarrot();
        });

        socket.on('mod_disabled', () => {
            this.requestGetCarrot();
        });

        this.requestGetCarrot();
    }

    handleRefreshClick = () => {
        this.requestGetCarrot();
    };

    handleInstallMoreClick = () => {
        this.props.onInstallMoreClick();
    };

    requestGetCarrot() {
        const socket = this.context;
        socket.emit('carrot status');
    }
}
