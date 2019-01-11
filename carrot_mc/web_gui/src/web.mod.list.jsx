import React from 'react';

import ModItem from './mod.item.jsx';

export default class WebModList extends React.Component {
    constructor(props) {
        super(props);

        this.state = { }
    }

    render() {
        return (
            <div className="container mod-list">
                {this.props.mods.map(mod => <ModItem key={mod.key} mod={mod} />)}
            </div>
        );
    }
}
