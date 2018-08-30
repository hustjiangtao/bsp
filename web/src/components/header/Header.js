import React, { Component } from "react";
import {Header, Navigation} from 'react-mdl';

class AppHeader extends Component {
  render() {
    return (
      <Header title="Title" scroll>
        <Navigation>
          <a href="">Link</a>
          <a href="">Link</a>
          <a href="">Link</a>
          <a href="">Link</a>
        </Navigation>
      </Header>
    );
  }
}

export default AppHeader;
