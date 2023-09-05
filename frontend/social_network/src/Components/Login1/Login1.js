import React from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik';
import axios from "axios";

import '../Login/login.scss'

export default function Login() {


    return (
        <Formik
            initialValues={{email: '', password: ''}}
            validate={values => {
                const errors = {}
                if (!values.email) {
                    errors.email = 'Обязательное поле'
                } else if (
                    !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
                ) {
                    errors.email = 'Неправильный email адрес'
                }
                if (!values.password) {
                    errors.password = "Обязательное поле"
                } else if (values.password.length < 8)
                    errors.password = "Пароль слишком короткий"
                return errors;
            }}
            onSubmit={(values, { setSubmitting }) => {
                 axios.post('https://jsonplaceholder.typicode.com/posts/', {
                    "userId": 102,
                    "id": 102,
                    "title": "title2",
                    "body": "bodyyy2"
                }).then(function (response) {
                    console.log(response.data)
                }).catch(function (error) {
                    console.log(error)
                })
                setSubmitting(false)
            }}>
            <div className="parent">
                <div className="block">
                    <h3>Вход</h3>
                <Form className="form">
                    <label htmlFor="email" className="label_email">Email</label>
                    <Field
                        id="email"
                        name="email"
                        type="email"
                        className="email"
                    />
                    <ErrorMessage className="error" name="email" component="div"/>
                    <label htmlFor="password" className="label_pass">Пароль</label>
                    <Field
                        id="password"
                        name="password"
                        type="password"
                        className="password"
                    />
                    <ErrorMessage className="error" name="password" component="div"/>
                    <label className="checkbox">
                    <Field
                        name="terms"
                        type="checkbox"/>
                        <span>Запомнить меня</span>
                    </label>
                    <button type="submit" className="button">Войти</button>
                    <div className="divider"></div>
                    <a href="../Login#" className="forget">Забыли пароль? </a>
                    <button type="button" className="google"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M18.1711 8.36788H17.4998V8.33329H9.99984V11.6666H14.7094C14.0223 13.607 12.1761 15 9.99984 15C7.23859 15 4.99984 12.7612 4.99984 9.99996C4.99984 7.23871 7.23859 4.99996 9.99984 4.99996C11.2744 4.99996 12.434 5.48079 13.3169 6.26621L15.674 3.90913C14.1857 2.52204 12.1948 1.66663 9.99984 1.66663C5.39775 1.66663 1.6665 5.39788 1.6665 9.99996C1.6665 14.602 5.39775 18.3333 9.99984 18.3333C14.6019 18.3333 18.3332 14.602 18.3332 9.99996C18.3332 9.44121 18.2757 8.89579 18.1711 8.36788Z" fill="#FFC107"/>
                        <path d="M2.62744 6.12121L5.36536 8.12913C6.10619 6.29496 7.90036 4.99996 9.99994 4.99996C11.2745 4.99996 12.4341 5.48079 13.317 6.26621L15.6741 3.90913C14.1858 2.52204 12.1949 1.66663 9.99994 1.66663C6.79911 1.66663 4.02327 3.47371 2.62744 6.12121Z" fill="#FF3D00"/>
                        <path d="M9.9998 18.3334C12.1523 18.3334 14.1081 17.5096 15.5869 16.17L13.0077 13.9875C12.1429 14.6452 11.0862 15.0009 9.9998 15C7.8323 15 5.99189 13.618 5.29855 11.6892L2.58105 13.783C3.96022 16.4817 6.76105 18.3334 9.9998 18.3334Z" fill="#4CAF50"/>
                        <path d="M18.1713 8.36796H17.5V8.33337H10V11.6667H14.7096C14.3809 12.5902 13.7889 13.3972 13.0067 13.988L13.0079 13.9871L15.5871 16.1696C15.4046 16.3355 18.3333 14.1667 18.3333 10C18.3333 9.44129 18.2758 8.89587 18.1713 8.36796Z" fill="#1976D2"/>
                    </svg>Продолжить с Google</button>
                    <button type="button" className="button button_register">Регистрация</button>
                </Form>
                </div>
            </div>
        </Formik>
    )
}