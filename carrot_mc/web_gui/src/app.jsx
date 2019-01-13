import React from 'react';
import * as _ from 'lodash';

import './app.css';

import WebModList from './web.mod.list';
import SocketContext from "./socket.context";
import InstalledModList from "./installed.mod.list";

export default class CarrotApp extends React.Component {
    static contextType = SocketContext;

    constructor(props) {
        super(props);

        this.state = {
            webListOpen: false,
            installedMods: [],
            installingMods: []
        };
    }

    render() {
        return (
            <div id="page-container" className="container">
                <div className="row">
                    <div className="col">
                        <InstalledModList
                            webListOpen={this.state.webListOpen}
                            onInstallMoreClick={this.handleInstallMoreClick}
                            onCarrotStatusChange={this.handleCarrotStatusChange} />
                    </div>
                    {this.state.webListOpen && <div className="col">
                        <WebModList
                            installedMods={this.state.installedMods}
                            installingMods={this.state.installingMods}
                            onCloseClick={this.handleWebCloseClick}
                            onModInstallClick={this.handleModInstallClick}
                        />
                    </div>}
                </div>
            </div>
        );
    }

    componentDidMount() {
        const socket = this.context;

        socket.on('info will_download_mod', mod_info => {
            let installing_mods = this.state.installedMods;
            installing_mods.push(mod_info.key);
            this.setState({ installingMods: installing_mods });
        });

        socket.on('info all_mod_install_complete', () => {
            socket.emit('carrot status');
        });
    }

    handleInstallMoreClick = () => {
        this.setState({ webListOpen: true });
    };

    handleWebCloseClick = () => {
        this.setState({ webListOpen: false });
    };

    handleCarrotStatusChange = (carrot_status) => {
        let mods = [];
        _.forEach(carrot_status.mods, (mod) => {
            mods.push(mod.key);
        });

        this.setState({ installedMods: mods });
    };

    handleModInstallClick = (mod) => {
        const socket = this.context;
        socket.emit('carrot install', { mod_key: [mod.key] });
    };
}
