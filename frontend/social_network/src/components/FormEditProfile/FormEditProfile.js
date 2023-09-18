import React from 'react';
import NavBar from "../NavBar/NavBar";
import {Col, Container, Row, Form, FormControl, Button} from "react-bootstrap";
import {useFormik} from "formik";
import axios from "axios";
import * as Yup from 'yup';
import 'bootstrap/dist/css/bootstrap.min.css'

import './formEditProfile.scss'

const FormEditProfile = () => {
    const formik = useFormik({
        initialValues: {
            firstName: '',
            lastName: '',
            phone: '',
            city: '',
            aboutMe: '',
            dateOfBirth: '',
            lifestyle: '',
            interest: ''
        },
        validationSchema: Yup.object({
            firstName: Yup.string().required("Обязательное поле"),
            lastName: Yup.string().required()
        }),
        //onSubmit: values => console.log(JSON.stringify(values, null, 2))
        onSubmit:(values) => {
            axios.put(`http://127.0.0.1:8000/api/v1/account/edit/`, {
                first_name: values.firstName,
                last_name: values.lastName,
                phone: values.phone,
                city: values.city,
                about_me: values.aboutMe,
                date_of_birth: values.dateOfBirth,
                lifestyle: values.lifestyle,
                interest: values.interest
            }).then(response => console.log(response.data))
                .catch(error => console.log(error))
        }
    })

    return (
        <>
            <NavBar/>
            <Container>
                <h2>Редактирование профиля</h2>
                <Form noValidate onSubmit={formik.handleSubmit}>
                    <Row className="mb-3">
                        <Col>
                            <Form.Group as={Col} md="3" controlId="validFormik1">
                                <Form.Label>Имя</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="firstName"
                                    value={formik.values.firstName}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.firstName && ! formik.errors.firstName}
                                />
                                <FormControl.Feedback>Looks good!</FormControl.Feedback>
                            </Form.Group>
                            <Form.Group as={Col} md="3" controlId="validFormik2">
                                <Form.Label>Фамилия</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="lastName"
                                    value={formik.values.lastName}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.lastName && ! formik.errors.lastName}
                                />
                                <FormControl.Feedback>Looks good!</FormControl.Feedback>
                            </Form.Group>
                            <Form.Group as={Col} md="3" controlId="validFormik3">
                                <Form.Label>Номер телефона</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="phone"
                                    value={formik.values.phone}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.phone && !formik.errors.phone}
                                />
                                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                            </Form.Group>
                            <Form.Group as={Col} md="3" controlId="validFormik4">
                                <Form.Label>Город</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="city"
                                    value={formik.values.city}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.city && !formik.errors.city}
                                />
                                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                            </Form.Group>
                            <Form.Group as={Col} md="3" controlId="validFormik5">
                                <Form.Label>Дата рождения</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="dateOfBirth"
                                    value={formik.values.dateOfBirth}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.dateOfBirth && !formik.errors.dateOfBirth}
                                />
                                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                            </Form.Group>
                            <Form.Group as={Col} md="3" controlId="validFormik6">
                                <Form.Label>Статус</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="aboutMe"
                                    value={formik.values.aboutMe}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.aboutMe && !formik.errors.aboutMe}
                                />
                            </Form.Group>
                            <Form.Group as={Col} md="3" controlId="validFormik7">
                                <Form.Label>Стиль жизни</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="lifestyle"
                                    value={formik.values.lifestyle}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.lifestyle && !formik.errors.lifestyle}
                                />
                            </Form.Group>
                            <Form.Group as={Col} md="3" controlId="validFormik8">
                                <Form.Label>Интересы</Form.Label>
                                <Form.Control
                                    type="text"
                                    name="interest"
                                    value={formik.values.interest}
                                    onChange={formik.handleChange}
                                    isValid={formik.touched.interest && !formik.errors.interest}
                                />
                            </Form.Group>
                        </Col>
                    </Row>
                    <Button type="submit">Сохранить изменения</Button>
                </Form>
            </Container>
        </>
    );
};

export default FormEditProfile;