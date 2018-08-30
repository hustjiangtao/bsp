import React, { Component } from 'react';
import {Button, Textfield} from 'react-mdl';
import './Login.css';

class Login extends Component {
  render() {
    return (
      <div className="Login mdl-card mdl-card__actions">
        <form>
          <Textfield label="Username" floatingLabel/>
          <Textfield label="Password" floatingLabel/>
          <Button className="Login-button" raised colored ripple>Login</Button>
          <Button className="Login-button" raised ripple>Register</Button>
        </form>
      </div>
    );
  }
}

export default Login;
