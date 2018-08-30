import React, { Component } from 'react';
import {Layout} from 'react-mdl';
import './App.css';
import AppHeader from './components/header/Header';
import AppDrawer from './components/header/Drawer';
import AppFooter from './components/footer/Footer';
import Login from './components/auth/Login';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Layout>
          <AppHeader/>
          <AppDrawer/>
          <Login/>
          {/*<AppFooter/>*/}
        </Layout>
      </div>
    );
  }
}

export default App;
