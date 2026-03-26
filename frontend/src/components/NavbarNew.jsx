import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          🚀 AI Career Guidance
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              Home
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/skills" className="nav-link">
              Skills
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/quiz" className="nav-link">
              Quiz
            </Link>
          </li>
          <li className="nav-item">
            <Link to="/results" className="nav-link">
              Results
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
