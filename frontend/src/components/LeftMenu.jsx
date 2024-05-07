import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const LeftMenu = ({ pages }) => {
  const location = useLocation();

  if (!pages || pages.length === 0) {
    return null; // Render nothing if pages are not defined or empty
  }

  return (
    <div className="left-menu">
      <ul>
        {pages.map((page, index) => (
          <li key={index} className={location.pathname === page.path ? 'active' : ''}>
            <Link to={page.path}>{page.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LeftMenu;
