import React, {useEffect, useState} from 'react';
import {Link} from "react-router-dom"
import NavBar from "../NavBar/NavBar";
import {getUser} from "../../services/UserService";
import {Container, Nav, Row, Col, Image} from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css'

import './home.scss'

const Home = () => {
    const [user, setUser] = useState('')


    useEffect(() => {
        updateUser()
    }, [])

    const updateUser = () => {
        getUser().then(userLoad)
    }
    const userLoad = (user) => {
        setUser(user)
    }
    console.log(user)

    return (
        <>
        <NavBar/>
        <main>
          <Container>
              <Row>
                  <Col>
                      <Nav defaultActiveKey="/account/im" className="flex-column">
                      <Nav.Link href="/account/im">Моя страница</Nav.Link>
                      <Nav.Link href="/feed">Новости</Nav.Link>
                      <Nav.Link href="/chat">Мессенджер</Nav.Link>
                      <Nav.Link href="/friends">Друзья</Nav.Link>
                      <Nav.Link href="/groups">Сообщества</Nav.Link>
                      <Nav.Link href="/albums">Фотографии</Nav.Link>
                      </Nav>
                  </Col>
                  <Col className="pt-3" xs = {3}>
                      <div className="wrapper_col2">
                        <div className="avatar">
                            <Image src="avatar.jpg" fluid rounded alt="avatar"/>
                        </div>
                          <Link to="/account/edit" className="btn btn_edit" type="button">Редактировать профиль</Link>
                      </div>
                  </Col>
                  <Col className="pt-3" xs = {7}>
                      <div className="wrapper_col3">
                        <div className="about">
                            <div className="about_name">{`${user.firstName} ${user.lastName}`}</div>
                            <div className="divider"></div>
                            <div className="about_me">
                                <label>День рождения:</label><br/>
                                <label>Город:</label>
                            </div>
                        </div>
                      </div>
                  </Col>
              </Row>
          </Container>
      </main>
        </>
  );
};

export default Home;