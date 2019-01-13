import React from 'react';

import './mod.info.modal.css';

export default class ModInfoModal extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="modal-background">
                <div className="container modal-main">
                    <div className="row">
                        <div className="col-auto mr-auto">
                            <span className="mod-key" onClick={this.openModInfo}>[{this.props.mod.key}]</span>
                            <br/>
                            <span className="mod-name">{this.props.mod.name}</span>
                            {' by '}
                            <span className="mod-owner">{this.props.mod.owner}</span>
                        </div>

                        <div className="col-auto">
                            <button type="button" className="btn btn-outline-warning" onClick={this.props.onCloseClicked}>
                                Close
                            </button>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col mod-description" dangerouslySetInnerHTML={this.descriptionMarkup()} />
                    </div>
                </div>
            </div>
        );
    }

    descriptionMarkup() {
        return { __html: this.props.mod.description };
    }
}