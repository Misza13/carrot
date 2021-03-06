import React from 'react';

import './installed.mod.item.css';

import SocketContext from "./socket.context";

export default class InstalledModItem extends React.Component {
    static contextType = SocketContext;

    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div className="row mod-info-row">
                <div className="col">
                    <div className="row">
                        <div className="col-8 col-md-9 col-lg-10">
                            <span className="mod-key">[{this.props.mod.key}]</span>
                            <br/>
                            <span className="mod-name">{this.props.mod.name}</span>
                            {' by '}
                            <span className="mod-owner">{this.props.mod.owner}</span>
                        </div>
                        <div
                            className="col-4 col-md-3 col-lg-2"
                            title={this.props.mod.disabled ? "Disabled" : "Enabled"}
                            >
                            <div className="form-check checkbox-slider--b enable-slider">
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={this.props.mod.disabled ? "" : "checked"}
                                        onChange={this.handleEnableClick} />
                                    <span>&nbsp;</span>
                                </label>
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-auto ml-auto">
                            {this.props.mod.file_missing &&
                                <div className="msg-error">
                                    File&nbsp;missing!
                                </div>}
                            {!this.props.mod.file_missing &&
                             this.isFileCorrupted(this.props.mod) &&
                                <div className="msg-error">
                                    File&nbsp;corrupted!
                                </div>}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
    
    isFileCorrupted(mod) {
        return mod.actual_file_md5 !== mod.file.file_md5;
    }

    handleEnableClick = () => {
        const socket = this.context;

        if (this.props.mod.disabled) {
            socket.emit('carrot enable', { mod_key: [this.props.mod.key] });
        } else {
            socket.emit('carrot disable', { mod_key: [this.props.mod.key] });
        }
    }
}