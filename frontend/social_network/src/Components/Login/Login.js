import React from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik';
import 'bootstrap/dist/css/bootstrap.min.css'
import './login.scss'

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
                setTimeout(() => {
                alert(JSON.stringify(values, null, 2));
                setSubmitting(false);
                }, 400);
       }}>
            <Form className="form">
                <label htmlFor='email' className="form-label">Email address</label>
                <Field
                    id="email"
                    name="email"
                    type="email"
                    className="form-control"
                    placeholder="name@example.com"
                />
                <ErrorMessage className="error" name="email" component="div"/>
                <label htmlFor='password' className="form-label">Password</label>
                <Field
                    id="password"
                    name="password"
                    type="password"
                    className="form-control"
                />
                <div className="form-text">
                    Your password must be 8-20 characters long
                </div>
                <ErrorMessage className="error" name="password" component="div"/>
                <button type="submit" className="btn btn-primary">Войти</button>
            </Form>
        </Formik>
    )
}

// import React from 'react'
// import {Form, Button} from 'react-bootstrap';
// import '../../../node_modules/bootstrap/dist/css/bootstrap.min.css'
// import { Formik } from 'formik';

// export default function Login() {
//   return (
//     <div>
//      <h1>Anywhere in your app!</h1>
//      <Formik
//        initialValues={{ email: '', password: '' }}
//        validate={values => {
//          const errors = {};
//          if (!values.email) {
//            errors.email = 'Required';
//          } else if (
//            !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)
//          ) {
//            errors.email = 'Invalid email address';
//          }
//          return errors;
//        }}
//        onSubmit={(values, { setSubmitting }) => {
//          setTimeout(() => {
//            alert(JSON.stringify(values, null, 2));
//            setSubmitting(false);
//          }, 400);
//        }}
//      >
//        {({
//          values,
//          errors,
//          touched,
//          handleChange,
//          handleBlur,
//          handleSubmit,
//          isSubmitting,
//          /* and other goodies */
//        }) => (
//          <form onSubmit={handleSubmit}>
//            <input
//              type="email"
//              name="email"
//              onChange={handleChange}
//              onBlur={handleBlur}
//              value={values.email}
//            />
//            {errors.email && touched.email && errors.email}
//            <input
//              type="password"
//              name="password"
//              onChange={handleChange}
//              onBlur={handleBlur}
//              value={values.password}
//            />
//            {errors.password && touched.password && errors.password}
//            <button type="submit" disabled={isSubmitting}>
//              Submit
//            </button>
//          </form>
//        )}
//      </Formik>
//    </div>
      
    
//   )
// }
