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

        socket.on('info will_download_mod', (info) => {
            let installing_mods = this.state.installingMods.slice();
            installing_mods.push(info.mod.key);

            this.setState({
                installingMods: installing_mods
            });
        });

        socket.on('info all_mod_install_complete', (info) => {
            const installed_list = info.installed_list;

            let installing_mods = this.state.installingMods.slice();
            _.remove(installing_mods, m => _.includes(installed_list, m));

            let installed_mods = this.state.installedMods.slice().concat(installed_list);

            this.setState({
                installingMods: installing_mods,
                installedMods: installed_mods
            });
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
        let installing_mods = this.state.installingMods.slice();
        installing_mods.push(mod.key);
        this.setState({
            installingMods: installing_mods
        }, () => {
            const socket = this.context;
            socket.emit('carrot install', {mod_key: [mod.key]});
        });
    };
}
