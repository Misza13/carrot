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
                <div className="col-9 col-lg-10">
                    <div className="row">
                        <div className="col">
                            <span className="mod-key">[{this.props.mod.key}]</span>
                            <br/>
                            <span className="mod-name">{this.props.mod.name}</span>
                            {' by '}
                            <span className="mod-owner">{this.props.mod.owner}</span>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}