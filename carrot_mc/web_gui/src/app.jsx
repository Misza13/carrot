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
            installedMods: []
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
                            onCloseClick={this.handleWebCloseClick} />
                    </div>}
                </div>
            </div>
        );
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
}
