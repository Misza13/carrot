import React from 'react';

import WebModItem from './web.mod.item';
import SocketContext from "./socket.context";

import './web.mod.list.css';

export default class WebModList extends React.Component {
    static contextType = SocketContext;

    constructor(props) {
        super(props);

        this.state = {
            mods: [],
            isLoadingMore: false
        }
    }

    render() {
        return (
            <div className="container mod-list">
                <div className="row">
                    <div className="col">
                        <div className="btn-group web-mods-toolbar" role="group">
                            <button
                                type="button"
                                className="btn btn-outline-warning"
                                onClick={this.handleCloseWebClick}>
                                Close
                            </button>
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col web-mods-col">
                        {this.state.mods.map(mod => <WebModItem key={mod.key} mod={mod} />)}

                        {this.state.isLoadingMore && <div className="row">
                            <div className="col loading">

                            </div>
                        </div>}
                    </div>
                </div>
            </div>
        );
    }

    componentDidMount() {
        const socket = this.context;

        socket.on('carrot search', result => {
            this.setState({ mods: result }); //TODO: Paged results should concat
            this.setState({ isLoadingMore: false });
        });

        socket.emit('carrot search', { mod_key: '', mc_version: '1.12.2' }); //TODO: hardcoded version

        this.setState({ isLoadingMore: true });
    }

    handleCloseWebClick = () => {
        this.props.onCloseClick();
    };
}
