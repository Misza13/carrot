import React from 'react';

import WebModItem from './web.mod.item';
import SocketContext from "./socket.context";

export default class WebModList extends React.Component {
    static contextType = SocketContext;

    constructor(props) {
        super(props);

        this.state = {
            mods: []
        }
    }

    render() {
        return (
            <div className="container mod-list">
                {this.state.mods.map(mod => <WebModItem key={mod.key} mod={mod} />)}
            </div>
        );
    }

    componentDidMount() {
        const socket = this.context;
        socket.on('carrot search', result => {
            this.setState({ mods: result });
        });

        socket.emit('carrot search', { mod_key: '', mc_version: '1.12.2' }); //TODO: hardcoded version
    }
}
