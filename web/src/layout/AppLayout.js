import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom';

// 引入模块组件
import AppHeader from '../components/header/Header';
// import Home from './components/home.js';
import Login from '../components/auth/Login';

// 引入样式文件
import '../App.css';

// 引入路由
import createHistory from 'history/createBrowserHistory';
const history = createHistory();

// 开始代码
class AppLayout extends Component {
  render() {
    return (
      <div className="App-layout">
        {/*路由配置*/}
        <Router history = {history}>
          <div className="App-contentBox">
            {/*编写导航*/}
            <AppHeader/>
            {/*路由匹配*/}
            <div className="App-content">
              <Switch>
                <Route exact path="/" component={Login}/>
                <Route path="/plan" component={Login}/>
                {/*<Route path="/detail/:id" component={Detail}/>*/}
              </Switch>
            </div>
          </div>
        </Router>
      </div>
    );
  }
}

export default AppLayout;