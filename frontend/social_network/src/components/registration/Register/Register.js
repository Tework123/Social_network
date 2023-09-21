import {useFormik} from "formik";
import axios from "../../../api/axios";

import './register.scss';
import React, {useState} from "react";
import * as Yup from "yup";
import NavBar from "../../NavBar/NavBar";
import {Button, Col, Container, Form, Row} from "react-bootstrap";

export default function Register() {
    const [errorMsg, setErrorMes] = useState('')

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
                .min(5,'Минимум 5 символов')
                .required('Обязательное поле')
        }),
        onSubmit: values => {
            axios.post('http://127.0.0.1:8000/api/v1/login/register/', {
                email: values.email,
                password: values.password
            }).then(function (response) {
                alert(response.data)
                console.log(response.data)
            }).catch(function (error) {
                console.log(error)
                if (error) {
                    setErrorMes("Ошибка")
                }
            })
        }
    })

    return (
        <>
            <NavBar/>
            <section>
                <Form onSubmit={formik.handleSubmit}>
                    <Container>
                        <Row className="pt-4">
                            <Col className="form_reg" md={{span: 3, offset: 4}}>
                                 <h2 className="text-center">Регистрация</h2>
                                <Form.Group>
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
                                <Form.Group>
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
                                <Button className="mt-3 btn_reg" type="submit">Зарегистрироваться</Button>
                            </Col>
                        </Row>
                    </Container>
                </Form>
            </section>
        </>
    )
}