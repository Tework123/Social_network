import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Link,
  Switch 
} from "react-router-dom";
import { Navbar, Container, Nav } from "react-bootstrap";
import Register from '../Register/Register'
import Login from "../Login/Login";
import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css'


export default function Sidebar() {
  return (
    <Router>
    <div>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/register">Register</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
          <li>
            <Link to="/users">Users</Link>
          </li>
        </ul>
      </nav>

    
      <Switch>
        <Route path="/register">
          <Register />
        </Route>
        <Route path="/login">
          <Login />
        </Route>
        <Route path="/users">
          <Users />
        </Route>
        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </div>
  </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}


function Users() {
  return <h2>Users</h2>;
}
