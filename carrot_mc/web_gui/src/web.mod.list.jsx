import React from 'react';

import WebModItem from './web.mod.item';

export default class WebModList extends React.Component {
    constructor(props) {
        super(props);

        this.state = { }
    }

    render() {
        return (
            <div className="container mod-list">
                {this.props.mods.map(mod => <WebModItem key={mod.key} mod={mod} />)}
            </div>
        );
    }
}
