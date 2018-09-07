import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import App from './App';
import registerServiceWorker from './registerServiceWorker';
import 'react-mdl/extra/material.min.css';
import 'react-mdl/extra/material.min.js';
// import Login from "./components/auth/Login";
import request from "./utils/request";

// ReactDOM.render(<App />, document.getElementById('root'));


class AuthForm extends React.Component {
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
  render() {
    const isLoggedIn = this.state.isLoggedIn;

    let auth_form = '';
    if (isLoggedIn) {
      auth_form = (
        <form>
          <label>
            Account:
            <input type={"text"} name={"account"} value={this.state.account} onChange={this.handleAccountChange}/>
          </label>
          <br/>
          <label>
            Password:
            <input type={"password"} name={"password"} value={this.state.password} onChange={this.handlePasswordChange}/>
          </label>
          <br/>
          <button type={"button"} value={"Login"} onClick={this.handleLogin}>Login</button>
          <input type={"button"} value={"To Register"}/>
        </form>
      );
    } else {
      auth_form = (
        <form>
          <label>
            Account:
            <input type={"text"} name={"account"} value={this.state.account} onChange={this.handleAccountChange}/>
          </label>
          <br/>
          <label>
            Password:
            <input type={"password"} name={"password"} value={this.state.password} onChange={this.handlePasswordChange}/>
          </label>
          <br/>
          <label>
            Password Confirm:
            <input type={"password"} name={"password_confirm"} value={this.state.password_confirm} onChange={this.handlePasswordConfirmChange}/>
          </label>
          <br/>
          <input type={"submit"} value={"Register"}/>
          <input type={"button"} value={"To Login"}/>
        </form>
      );
    }
    return (
      auth_form
    )
  }
}

ReactDOM.render(
  <AuthForm/>,
  document.getElementById('root')
);
registerServiceWorker();
