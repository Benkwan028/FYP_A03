import React from "react";
import { Link } from "react-router-dom";
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container">
        <a className="navbar-brand" href="/">Motor 2nd seller</a>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item"><a className="nav-link" href="/">Home</a></li>
            <li className="nav-item"><a className="nav-link" href="/about">About Us</a></li>
            <li className="nav-item"><a className="nav-link" href="/shop">Shop</a></li>
            <li className="nav-item"><a className="nav-link" href="/blog">Blog</a></li>
            <li className="nav-item"><a className="nav-link" href="/login">Login</a></li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;