import React from 'react';
import logo from './logo.jpg'
import './NavBar.css';

const NavBar = () => {
  return (
    <div className="navbar">
      <img style={{ height: '100px' }} src={logo} alt="Logo" />
    </div>
  );
};

export default NavBar;
