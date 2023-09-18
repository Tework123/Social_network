import React, {useEffect, useState} from 'react';
import {Container, Nav, Row, Col, Image} from "react-bootstrap";
import {Link, useParams} from "react-router-dom"
import 'bootstrap/dist/css/bootstrap.min.css'
import NavBar from "../NavBar/NavBar";
import axios from "axios";

import './home.scss'
import {getUser} from "../../services/UserService";

const Home = () => {
    const [user, setUser] = useState('')
    const {userId} = useParams()

    useEffect(() => {
        updateUser()
    }, [userId])

    const updateUser = () => {
        getUser(userId).then(userLoad)
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
                      <Nav defaultActiveKey="/home" className="flex-column">
                      <Nav.Link href="/home">Моя страница</Nav.Link>
                      <Nav.Link href="/feed">Новости</Nav.Link>
                      <Nav.Link href="/im">Мессенджер</Nav.Link>
                      <Nav.Link href="/friends">Друзья</Nav.Link>
                      <Nav.Link href="/groups">Сообщества</Nav.Link>
                      <Nav.Link href="/albums">Фотографии</Nav.Link>
                      </Nav>
                  </Col>
                  <Col className="pt-3" xs = {3}>
                      <div className="wrapper_col2">
                        <div className="avatar">
                            <Image src="avatar.jpg" fluid rounded />
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