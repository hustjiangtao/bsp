import React, { Component } from "react";
import {Drawer, Navigation} from 'react-mdl';

class AppDrawer extends Component {
  render() {
    return (
      <Drawer title="Title">
        <Navigation>
          <a href="">Link</a>
          <a href="">Link</a>
          <a href="">Link</a>
          <a href="">Link</a>
        </Navigation>
      </Drawer>
    );
  }
}

export default AppDrawer;
