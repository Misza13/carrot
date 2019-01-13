import React from 'react';

import './web.mod.item.css';

import ModInfoModal from "./mod.info.modal";

export default class WebModItem extends React.Component {
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
                            {!this.props.isInstalled && !this.props.isInstalling && <button
                                type="button"
                                className="btn btn-outline-primary btn-sm btn-install"
                                title="Install"
                                onClick={this.handleInstallClick}>
                                <i className="fas fa-download" />
                            </button>}
                            {this.props.isInstalling && <div
                                className="btn btn-outline-success btn-sm btn-installing"
                                title="Installation in progress...">
                            </div>}
                            {this.props.isInstalled && <div
                                className="btn btn-outline-success btn-sm"
                                title="Mod is installed">
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

    handleInstallClick = () => {
        if (this.props.onInstallClick) {
            this.props.onInstallClick(this.props.mod);
        }
    };

    openModInfo = () => {
        this.setState({ modInfoOpen: true });
    };

    closeModInfo = () => {
        this.setState({ modInfoOpen: false });
    };
}