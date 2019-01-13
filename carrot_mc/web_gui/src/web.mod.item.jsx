import React from 'react';

import './web.mod.item.css';

import SocketContext from "./socket.context";
import ModInfoModal from "./mod.info.modal";

export default class WebModItem extends React.Component {
    static contextType = SocketContext;

    constructor(props) {
        super(props);

        this.state = {
            modInfoOpen: false
        };
    }

    render() {
        return (
            <div className="row mod-info-row">
                {this.state.modInfoOpen &&
                    <ModInfoModal
                        mod={this.props.mod}
                        onCloseClicked={this.closeModInfo} />
                }

                <div className="col-3 col-lg-2">
                    <img src={this.props.mod.avatar} alt={this.props.mod.name} />
                </div>

                <div className="col-8 col-lg-9">
                    <div className="row">
                        <div className="col-10">
                            <span className="mod-key help-active" onClick={this.openModInfo}>[{this.props.mod.key}]</span>
                            <br/>
                            <span className="mod-name">{this.props.mod.name}</span>
                            {' by '}
                            <span className="mod-owner">{this.props.mod.owner}</span>
                        </div>

                        <div className="col-2">
                            <button
                                type="button"
                                className="btn btn-outline-primary btn-sm"
                                title="Mod info"
                                onClick={this.openModInfo}>
                                <i className="fas fa-info-circle" />
                            </button>
                            {!this.props.isInstalled && <button
                                type="button"
                                className="btn btn-outline-primary btn-sm btn-install"
                                title="Install"
                                onClick={this.handleInstallClick}>
                                <i className="fas fa-download" />
                            </button>}
                            {this.props.isInstalled && <div
                                className="btn btn-outline-success btn-sm"
                                title="Installed">
                                <i className="fas fa-check" />
                            </div>}
                        </div>
                    </div>
                    <div className="row">
                        <div className="col">
                            <span className="mod-blurb">{this.props.mod.blurb}</span>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    componentDidMount() {
        const socket = this.context;
        socket.on('info all_mod_install_complete', () => {
            socket.emit('carrot status');
        });
    }

    handleInstallClick = () => {
        const socket = this.context;
        socket.emit('carrot install', { mod_key: [this.props.mod.key] });
    };

    openModInfo = () => {
        this.setState({ modInfoOpen: true });
    };

    closeModInfo = () => {
        this.setState({ modInfoOpen: false });
    };
}