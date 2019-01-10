function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

const SocketContext = React.createContext();

class InternetMod extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.handleInstallClick = this.handleInstallClick.bind(this);
  }

  handleInstallClick(e) {
    const socket = this.context;
    socket.emit('install', {
      mod_key: this.props.mod.key
    });
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
      className: "col-9 col-lg-10"
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
    }, this.props.mod.blurb)))), React.createElement("div", {
      className: "col-1"
    }, React.createElement("button", {
      type: "button",
      className: "btn btn-outline-primary btn-install",
      title: "Install",
      onClick: this.handleInstallClick
    }, React.createElement("i", {
      className: "fas fa-download"
    }))));
  }

}

_defineProperty(InternetMod, "contextType", SocketContext);

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

const socket = io('http://localhost:5000/');
ReactDOM.render(React.createElement(SocketContext.Provider, {
  value: socket
}, React.createElement(CarrotApp, null)), document.getElementById('root'));
