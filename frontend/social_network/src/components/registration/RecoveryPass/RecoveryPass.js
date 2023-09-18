import React from 'react';
import {ErrorMessage, Field, Form, Formik} from "formik";
import {useParams} from "react-router-dom";
import axios from "../../api/axios";

const RecoveryPass = () => {
    const token = useParams()

    axios.get(`/api/v1/login/reset_password/${token.uidb64}/${token.token}/`)
        .then(res => console.log(`then ${res.data}`))
        .catch(res => console.log(`catch ${res}`))

    return (
        <Formik
            initialValues={{password: ''}}
            validate={values => {
                const errors = {}
                if (!values.password) {
                    errors.password = "Обязательное поле"
                } else if (values.password.length < 8)
                    errors.password = "Пароль слишком короткий"
                return errors
            }}
            onSubmit={(values) => {
                console.log(values)
                axios.post(`http://127.0.0.1:8000/api/v1/login/reset_password/${token.uidb64}/${token.token}/`,{
                    password: values.password
                })
                .then(function (response) {
                    alert(response.data)
                    console.log(response.data)
                }).catch(error => console.log(error))
            }}>
            <div className="parent">
                <div className="block">
                    <h3>Введите новый пароль</h3>
                    <Form className="form">
                    <Field
                        name="password"
                        type="password"
                        className="password"
                    />
                    <ErrorMessage className="error" name="password" component="div"/>
                        <button type="submit" className="button">Восстановить пароль</button>
                    </Form>
                </div>
            </div>
        </Formik>
    );
};

export default RecoveryPass;