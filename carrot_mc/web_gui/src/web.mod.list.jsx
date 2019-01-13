import React from 'react';
import * as _ from 'lodash';

import './web.mod.list.css';

import WebModItem from './web.mod.item';
import SocketContext from "./socket.context";

export default class WebModList extends React.Component {
    static contextType = SocketContext;
    defaultPageSize = 20;

    constructor(props) {
        super(props);

        this.state = {
            mods: [],
            isLoadingMore: false,
            pageNum: 1,
            hasMore: true,
            searchMode: 'name',
            searchTerm: ''
        }
    }

    render() {
        return (
            <div className="container mod-list">
                <div className="row">
                    <div className="col">
                        <div className="input-group web-mods-toolbar" role="group">
                            {/* Search by dropdown */}
                            <div className="input-group-prepend">
                                <button type="button"
                                        className="btn btn-outline-secondary"
                                        data-toggle="dropdown"
                                        style={{width: "40px"}}>
                                    {this.state.searchMode === 'name' && <i className="far fa-file-alt" />}
                                    {this.state.searchMode === 'key' && <i className="fas fa-key" />}
                                    {this.state.searchMode === 'owner' && <i className="far fa-user" />}
                                </button>
                                <div className="dropdown-menu">
                                    <a className="dropdown-item" href="#" onClick={this.handleSearchByNameClick}>
                                        By name
                                    </a>
                                    <a className="dropdown-item" href="#" onClick={this.handleSearchByKeyClick}>
                                        By key
                                    </a>
                                    <a className="dropdown-item" href="#" onClick={this.handleSearchByOwnerClick}>
                                        By owner
                                    </a>
                                </div>
                            </div>

                            {/* Search input box */}
                            <input
                                type="text"
                                className="form-control"
                                value={this.state.searchTerm}
                                onChange={this.handleSearchInputChange}
                                onKeyUp={this.handleSearchKeyUp}/>

                            {/* Search button */}
                            <div className="input-group-append">
                                <button
                                    type="button"
                                    className="btn btn-outline-secondary"
                                    onClick={this.handleSearchSubmit}>
                                    <i className="fas fa-search" />
                                </button>
                            </div>

                            {/* Close web mods browsing button */}
                            <div className="input-group-append">
                                <button
                                    type="button"
                                    className="btn btn-outline-warning"
                                    onClick={this.handleCloseWebClick}>
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col web-mods-col" onScroll={this.handleScroll}>
                        {this.state.mods.map(mod =>
                            <WebModItem
                                key={mod.key}
                                mod={mod}
                                isInstalled={this.isModInstalled(mod.key)}
                            />)}

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
            const new_mods = this.state.mods.concat(result);

            this.setState({
                mods: new_mods,
                isLoadingMore: false,
                hasMore: result.length === this.defaultPageSize
            });
        });

        this.setState({ isLoadingMore: true });
        this.doSearch();
    }

    handleCloseWebClick = () => {
        this.props.onCloseClick();
    };

    handleScroll = (e) => {
        if (!this.state.isLoadingMore && this.state.hasMore) {
            const t = e.target;
            const remaining = t.scrollHeight - t.scrollTop - t.offsetHeight;

            if (remaining < 16) {
                this.setState({
                    isLoadingMore: true,
                    pageNum: this.state.pageNum + 1
                }, () => {
                    this.doSearch('');
                });
            }
        }
    };

    doSearch() {
        const socket = this.context;

        let searchObject = {
            mc_version: '1.12.2', //TODO: hardcoded version
            page_size: this.defaultPageSize,
            page_num: this.state.pageNum
        };

        switch (this.state.searchMode) {
            case 'name':
                searchObject.mod_name = this.state.searchTerm;
                break;
            case 'key':
                searchObject.mod_key = this.state.searchTerm;
                break;
            case 'owner':
                searchObject.owner = this.state.searchTerm;
                break;
        }

        socket.emit('carrot search', searchObject);
    }

    handleSearchByNameClick = () => {
        this.setState({ searchMode: 'name' });
    };

    handleSearchByKeyClick = () => {
        this.setState({ searchMode: 'key' });
    };

    handleSearchByOwnerClick = () => {
        this.setState({ searchMode: 'owner' });
    };

    handleSearchInputChange = (e) => {
        this.setState({ searchTerm: e.target.value });
    };

    handleSearchKeyUp = (e) => {
        if (e.which === 13) {
            this.handleSearchSubmit();
        }
    };

    handleSearchSubmit = () => {
        if (this.state.isLoadingMore) {
            return;
        }

        this.setState({
            mods: [],
            pageNum: 1,
            isLoadingMore: true
        }, () => {
            this.doSearch();
        });
    };

    isModInstalled(mod_key) {
        return _.includes(this.props.installedMods, mod_key);
    };
}
