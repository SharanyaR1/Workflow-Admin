import React from 'react';
import './Home.css';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home-page-container">
    <h2>Admin Panel</h2>
      <div className="buttons-container">
        <Link to= "/Upload">
          <button>Add / Modify Service</button>
        </Link>
        <Link to= "/Modify">
          <button>Manage Bundles</button>
        </Link>
      </div>
    </div>
  );
}

export default Home;