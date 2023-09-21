import React, {useContext, useState} from "react";
import {useFormik} from 'formik';
import {Link, Redirect} from 'react-router-dom';
import AuthContext from "../../../context/AuthProvider";
import NavBar from "../../NavBar/NavBar";
import axios from "../../../api/axios";
import * as Yup from 'yup'
import {Button, Col, Container, Form, Row} from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css'

import './login.scss';

export default function Login() {
    const {setAuth} = useContext(AuthContext)
    const [email, setEmail] = useState('')
    const [pass, setPass] = useState('')
    const [errorMsg, setErrorMes] = useState('')
    const [success, setSuccess] = useState(false)

    const formik = useFormik({
        initialValues: {
            email: '',
            password: ''
        },
        validationSchema: Yup.object({
            email: Yup.string()
                .email('Wrong email')
                .required('Обязательное поле'),
            password: Yup.string()
                .required('Обязательное поле')
        }),
        onSubmit: values => {
            axios.post('http://127.0.0.1:8000/api/v1/login/auth/', {
                     email: values.email,
                     password: values.password
                }).then(function (response) {
                    console.log(response.data)
                    setAuth({email, pass})
                    setEmail('')
                    setPass('')
                    setSuccess(true)
                }).catch(function (error) {
                    if (error.response.status === 404) {
                        setErrorMes('Неправильный email или пароль')
                    }
            })
        }
    })

    return (
        <>
            <NavBar/>
            {success ? (
                <section>
                    <Redirect to="/account/im"/>
                </section>
            ): (
                <section>
                    <Form onSubmit={formik.handleSubmit}>
                    <Container>
                        <Row className="pt-4">
                            <Col className="login_form" md={{span: 3, offset: 4}}>
                                 <h2 className="text-center">Вход</h2>
                                <Form.Group controlId="validFormik1">
                                    <Form.Label>Email</Form.Label>
                                    <Form.Control
                                        className="form-control"
                                        type="email"
                                        name="email"
                                        placeholder="name@mail.ru"
                                        value={formik.values.email}
                                        onChange={formik.handleChange}
                                    />
                                </Form.Group>
                                {formik.touched.email && formik.errors.email ? <div className="error_msg">{formik.errors.email}</div> : null}
                                <Form.Group controlId="validFormik2">
                                    <Form.Label>Пароль</Form.Label>
                                    <Form.Control
                                        className="form-control"
                                        type="password"
                                        name="password"
                                        value={formik.values.password}
                                        onChange={formik.handleChange}
                                    />
                                </Form.Group>
                                {formik.touched.password && formik.errors.password ? <div className="error_msg">{formik.errors.password}</div> : null}
                                <p className="error_msg">{errorMsg}</p>
                                <Button className="mt-3 btn_login" type="submit">Войти</Button>
                                <Link to="/register" className="mt-3 btn btn-success btn_reg" type="button">Зарегистрироваться</Link>
                            </Col>
                        </Row>
                    </Container>
                </Form>
                </section>
            )}
        </>
    )
}