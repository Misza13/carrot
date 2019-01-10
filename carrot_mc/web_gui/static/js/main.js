class InternetMod extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return React.createElement("div", {
      className: "row mod-info-row"
    }, React.createElement("div", {
      className: "col-2 col-lg-1"
    }, React.createElement("img", {
      src: this.props.mod.avatar,
      alt: this.props.mod.name
    })), React.createElement("div", {
      className: "col"
    }, React.createElement("div", {
      className: "row"
    }, React.createElement("div", {
      className: "col"
    }, React.createElement("span", {
      className: "mod-name"
    }, this.props.mod.name), ' ', React.createElement("span", {
      className: "mod-key"
    }, "[", this.props.mod.key, "]"), ' by ', React.createElement("span", {
      className: "mod-owner"
    }, this.props.mod.owner))), React.createElement("div", {
      className: "row"
    }, React.createElement("div", {
      className: "col"
    }, React.createElement("span", {
      className: "mod-blurb"
    }, this.props.mod.blurb)))));
  }

}

class ModList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return React.createElement("div", {
      className: "container mod-list"
    }, this.props.mods.map(mod => React.createElement(InternetMod, {
      key: mod.key,
      mod: mod
    })));
  }

}

class CarrotApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      mods: []
    };
  }

  render() {
    return React.createElement("div", {
      id: "page-container"
    }, React.createElement(ModList, {
      mods: this.state.mods
    }));
  }

  componentDidMount() {
    fetch('https://api.carrot-mc.xyz/prod/mods').then(response => response.json()).then(response => this.setState({
      mods: response.result
    }));
  }

}

ReactDOM.render(React.createElement(CarrotApp, null), document.getElementById('root'));
