import React from 'react';
import {Container, Navbar, NavDropdown} from "react-bootstrap";

const NavBar = () => {
    return (
        <>
            <Navbar bg="primary" className="nav_bar">
        <Container>
          <Navbar.Brand href="#home" className="text-white">
            <img
              alt=""
              src="https://react-bootstrap.github.io/img/logo.svg"
              width="30"
              height="30"
              className="d-inline-block align-top"
            />{' '}
            React Bootstrap
          </Navbar.Brand>
          <NavDropdown title="Аккаунт" id="basic-nav-dropdown" className="text-white">
            <NavDropdown.Item href="#action/3.1">Настройки</NavDropdown.Item>
            <NavDropdown.Item href="#action/3.2">Выход</NavDropdown.Item>
          </NavDropdown>
        </Container>
      </Navbar>
        </>
    );
};

export default NavBar;