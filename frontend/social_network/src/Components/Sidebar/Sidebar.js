import React from "react";
import {BrowserRouter as Router, Route, Link, Switch} from "react-router-dom";
import Register from '../Register/Register'
import Register2 from '../Register2/Register2'
import Login from "../Login/Login";
import Login2 from "../Login2/Login2";
import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import Login1 from '../Login1/Login1'

import 'bootstrap/dist/css/bootstrap.min.css'
import Verification from "../Verification/Verification";

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
            <Link to="/register2">Register2</Link>
          </li>
          <li>
            <Link to="/login">Login</Link>
          </li>
           <li>
            <Link to="/login1">Login1</Link>
          </li>
          <li>
            <Link to="/login2">Login2</Link>
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
        <Route path="/register2">
          <Register2 />
        </Route>
        <Route path="/login">
          <Login />
        </Route>
        <Route path="/login1">
          <Login1 />
        </Route>
        <Route path="/login2">
          <Login2 />
        </Route>
        <Route path="/users">
          <Users />
        </Route>
        <Route exact path="/api/v1/login/activate/:uidb64/:token">
          <Verification />
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
