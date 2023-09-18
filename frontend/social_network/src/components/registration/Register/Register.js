import {ErrorMessage, Field, Form, Formik} from "formik";
import axios from "../../api/axios";
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap'

import './register.scss';

export default function Register() {
    const div = document.createElement('div')

    return (
        <Formik
            initialValues={{email: '', password: ''}}
            validate={values => {
                const errors = {}
                if (!values.email) {
                    errors.email = 'Обязательное поле'
                } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)) {
                    errors.email = 'Неправильный email адрес'
                }
                if (!values.password) {
                    errors.password = "Обязательное поле"
                } else if (values.password.length < 8)
                    errors.password = "Пароль слишком короткий"
                return errors
            }}
            onSubmit={(values) => {
                axios.post('http://127.0.0.1:8000/api/v1/login/register/', {
                    email: values.email,
                    password: values.password
                }).then(function (response) {
                    //alert(response.data)
                    div.innerHTML = "<div class=\"modal fade\" id=\"confirmModal\" tabindex=\"-1\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\n" +
                        "  <div class=\"modal-dialog\">\n" +
                        "    <div class=\"modal-content\">\n" +
                        "      <div class=\"modal-header\">\n" +
                        "        <h1 class=\"modal-title fs-5\" id=\"exampleModalLabel\">Modal title</h1>\n" +
                        "        <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Close\"></button>\n" +
                        "      </div>\n" +
                        "      <div class=\"modal-body\">\n" +
                        "        {response.data}\n" +
                        "      </div>\n" +
                        "      <div class=\"modal-footer\">\n" +
                        "        <button type=\"button\" class=\"btn btn-secondary\" data-bs-dismiss=\"modal\">Close</button>\n" +
                        "        <button type=\"button\" class=\"btn btn-primary\">Save changes</button>\n" +
                        "      </div>\n" +
                        "    </div>\n" +
                        "  </div>\n" +
                        "</div>"
                    document.body.append(div)
                    //div.insertAdjacentHTML('')
                    console.log(response.data)
                }).catch(error => console.log(error))
            }}>
            <div className="parent">
                <div className="block">
                    <h2>Регистрация</h2>
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
                            <button type="submit" className="register" data-bs-toggle="modal" data-bs-target="#confirmModal">Зарегистрироваться</button>
                        </Form>
                </div>
            </div>
        </Formik>
    )
}