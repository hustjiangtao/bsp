import React, { Component } from "react";
import {Header, Navigation} from 'react-mdl';
import {Link} from 'react-router-dom';

class AppHeader extends Component {
  render() {
    return (
      <Header title="Title" scroll>
        <Navigation>
          <Link to="/">Link</Link>
          <Link to="/plan">Link</Link>
          <Link to="/plan1">Link</Link>
          <Link to="/love">Link</Link>
        </Navigation>
      </Header>
    );
  }
}

export default AppHeader;
