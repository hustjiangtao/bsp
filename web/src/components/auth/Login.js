import React, { Component } from 'react';
import {Button, Textfield} from 'react-mdl';
import './Login.css';
import request from "../../utils/request";

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoggedIn: true,
      account: '',
      password: '',
      password_confirm: '',
    }
  }
  handleAccountChange = (e) => {
    this.setState({account: e.target.value});
  };
  handlePasswordChange = (e) => {
    this.setState({password: e.target.value});
  };
  handlePasswordConfirmChange = (e) => {
    this.setState({password: e.target.value});
  };
  handleLogin = () => {
    const params = {
      headers: {
        "Authorization": 'Basic ' + btoa(this.state.account + ':' + this.state.password)
      },
    };
    request.get('/tokens', params)
      .then( res => (console.log(res)))
  };
  handleRegister = () => {
    console.log('register...');
  };
  handleFormChange = () => {
    if (document.querySelector(".Login")) {
      document.querySelector(".Login").classList.add("Register");
      document.querySelector(".Login").classList.remove("Login");
    } else {
      document.querySelector(".Register").classList.add("Login");
      document.querySelector(".Register").classList.remove("Register");
    }
    this.setState({
      isLoggedIn: !this.state.isLoggedIn,
      account: '',
      password: '',
      password_confirm: '',
    });
  };
  render() {
    const isLoggedIn = this.state.isLoggedIn;

    let auth_form = '';
    if (isLoggedIn) {
      auth_form = (
        <form>
          <Textfield
            label="Account"
            floatingLabel
            type={"text"}
            name={"account"}
            value={this.state.account}
            onChange={this.handleAccountChange}
          />
          <Textfield
            label="Password"
            floatingLabel
            type={"password"}
            name={"password"}
            value={this.state.password}
            onChange={this.handlePasswordChange}
          />
          <Button className="Login-button" raised colored ripple type={"button"} onClick={this.handleLogin}>Login</Button>
          <Button className="Login-button" raised ripple type={"button"} onClick={this.handleFormChange}>Register</Button>
        </form>
      );
    } else {
      auth_form = (
        <form>
          <Textfield
            label="Account"
            floatingLabel
            type={"text"}
            name={"account"}
            value={this.state.account}
            onChange={this.handleAccountChange}
          />
          <Textfield
            label="Password"
            floatingLabel
            type={"password"}
            name={"password"}
            value={this.state.password}
            onChange={this.handlePasswordChange}
          />
          <Textfield
            label="Password Confirm"
            floatingLabel
            type={"password"}
            name={"password_confirm"}
            value={this.state.password_confirm}
            onChange={this.handlePasswordConfirmChange}
          />
          <Button className="Login-button" raised colored ripple type={"button"} onClick={this.handleRegister}>Register</Button>
          <Button className="Login-button" raised ripple type={"button"} onClick={this.handleFormChange}>Login</Button>
        </form>
      );
    }
    return (
      <div className="Login mdl-card mdl-card__actions">
        {auth_form}
      </div>
    );
  }
}

export default Login;
