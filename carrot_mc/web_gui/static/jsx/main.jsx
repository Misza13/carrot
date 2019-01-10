class InternetMod extends React.Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div className="row mod-info-row">
                <div className="col-2 col-lg-1">
                    <img src={this.props.mod.avatar} alt={this.props.mod.name} />
                </div>
                <div className="col">
                    <div className="row">
                        <div className="col">
                            <span className="mod-name">{this.props.mod.name}</span>
                            {' '}
                            <span className="mod-key">[{this.props.mod.key}]</span>
                            {' by '}
                            <span className="mod-owner">{this.props.mod.owner}</span>
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
}

class ModList extends React.Component {
    constructor(props) {
        super(props);

        this.state = { }
    }

    render() {
        return (
            <div className="container mod-list">
                {this.props.mods.map(mod => <InternetMod key={mod.key} mod={mod} />)}
            </div>
        );
    }
}

class CarrotApp extends React.Component {
    constructor(props) {
        super(props);

        this.state = { mods: [] };
    }

    render() {
        return (
            <div id="page-container">
                <ModList mods={this.state.mods} />
            </div>
        );
    }

    componentDidMount() {
        fetch('https://api.carrot-mc.xyz/prod/mods')
            .then(response => response.json())
            .then(response => this.setState({ mods: response.result }));
    }
}

ReactDOM.render(
    <CarrotApp />,
    document.getElementById('root')
);