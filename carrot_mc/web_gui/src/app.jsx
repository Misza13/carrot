import React from 'react';

import WebModList from './web.mod.list.jsx';

export default class CarrotApp extends React.Component {
    constructor(props) {
        super(props);

        this.state = { mods: [] };
    }

    render() {
        return (
            <div id="page-container">
                <WebModList mods={this.state.mods} />
            </div>
        );
    }

    componentDidMount() {
        fetch('https://api.carrot-mc.xyz/prod/mods')
            .then(response => response.json())
            .then(response => this.setState({ mods: response.result }));
    }
}
