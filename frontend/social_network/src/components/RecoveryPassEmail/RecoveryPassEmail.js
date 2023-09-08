import {ErrorMessage, Field, Form, Formik} from "formik";
import axios from "axios";

const RecoveryPassEmail = () => {

    return (
        <Formik
            initialValues={{email: ''}}
            validate={values => {
                const errors = {}
                if (!values.email) {
                    errors.email = 'Обязательное поле'
                } else if (
                    !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
                ) {
                    errors.email = 'Неправильный email адрес'
                }
                return errors
            }}
            onSubmit={(values) => {
                console.log(values)
                axios.post(`http://127.0.0.1:8000/api/v1/login/reset_password/`,{
                    email: values.email
                })
                .then(function (response) {
                    alert(response.data)
                    console.log(response.data)
                }).catch(error => console.log(error))
            }}>
            <div className="parent">
                <div className="block">
                    <h3>Введите почту для восстановления пароля</h3>
                    <Form className="form">
                        <label htmlFor="email" className="label_email">Email</label>
                        <Field
                            id="email"
                            name="email"
                            type="email"
                            className="email"
                        />
                        <ErrorMessage className="error" name="email" component="div"/>
                        <button type="submit" className="button">Восстановить пароль</button>
                    </Form>
                </div>
            </div>
        </Formik>
    )
}

export default RecoveryPassEmail;