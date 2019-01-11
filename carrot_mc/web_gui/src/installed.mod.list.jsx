import React from 'react';

import InstalledModItem from "./installed.mod.item";

export default class InstalledModList extends React.Component {
    constructor(props) {
        super(props);

        this.state = { }
    }

    render() {
        return (
            <div className="container mod-list">
                {this.props.mods.map(mod => <InstalledModItem key={mod.key} mod={mod} />)}
            </div>
        );
    }
}
