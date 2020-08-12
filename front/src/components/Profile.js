import React, { Component } from 'react';
import { connect } from 'react-redux';
import { NavLink } from 'react-router-dom';

class Profile extends Component {
    state = {
        selectedOption: null
    }

    escape = () => {
        if (this.state.selectedOption)
            return;
        this.props.togglePop();
    }
    
    changer = (event) => {
        let nextState = {};
        nextState[event.target.name] = event.target.value;
        this.setState(nextState);
    }

    renderUser() {
        const {username, email} = this.props.user;

        return (
            <div className="profile-user-box">
                <h3 className="profile-item">
                    {username}
                </h3>
                <label className="profile-item"
                style={{
                    fontSize: '70%',
                    color: 'darkgray'}}>
                    {email}
                </label>
            </div>
        );
    }

    renderOption() {
        return (
            <div className="profile-option-box">
                <p id="1" 
                onClick={(e)=>this.setState({selectedOption: e.target.id})}>
                    테스트
                </p>
            </div>
        )
    }

    renderLogoutIcon() {
        return (<svg
        width="24" height="24" viewBox="0 0 24 24">
        <path d="M16 12.771h-3.091c-.542 0-.82-.188
        -1.055-.513l-1.244-1.674-2.029 2.199 1.008 
        1.562c.347.548.373.922.373 1.42v4.235h-1.962v
        -3.981c-.016-1.1-1.695-2.143-2.313-1.253l-1.176 
        1.659c-.261.372-.706.498-1.139.498h-3.372v
        -1.906l2.532-.001c.397 0 .741-.14.928-.586l1.126
        -2.75c.196-.41.46-.782.782-1.102l2.625-2.6
        -.741-.647c-.223-.195-.521-.277-.812-.227l
        -2.181.381-.342-1.599 2.992-.571c.561-.107 
        1.042.075 1.461.462l2.882 2.66c.456.414.924 
        1.136 1.654 2.215.135.199.323.477.766.477h2.328v1.642zm
        -2.982-5.042c1.02-.195 1.688-1.182 1.493
        -2.201-.172-.901-.96-1.528-1.845-1.528-1.186 
        0-2.07 1.078-1.85 2.234.196 1.021 1.181 1.69 
        2.202 1.495zm4.982-5.729v15l6 5v-20h-6z"/></svg>);
    }

    renderLogout() {
        return (
            <NavLink to="/logout"
            className="profile-logout"
            onClick={this.props.togglePop}>
                {this.renderLogoutIcon()}
                로그아웃
            </NavLink>
        );
    }

    renderEdit() {
        return (
            <div className="profile-edit-box"
            onClick={e=>e.stopPropagation()}>
                <button 
                onClick={()=>{this.setState({selectedOption: null});}}>
                    asdf
                </button>
                asdfasdfasdf
            </div>
        )
    }

    render() {
        return(
            <div 
            className="profile-modal" 
            onClick={this.escape}>
                {this.state.selectedOption && this.renderEdit()}
                <div
                className="profile-modal-content"
                onClick={(e)=>{e.stopPropagation();}}>
                    {this.renderUser()}
                    {this.renderOption()}
                    {this.renderLogout()}
                </div>
            </div>
        )
    }
}

export default connect((state) => {
    return {
        user: state.userReducer.user
    };
}, {})(Profile);

