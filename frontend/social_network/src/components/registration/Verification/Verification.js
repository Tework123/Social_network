import {Redirect, useParams} from "react-router-dom";
import axios from "../../../api/axios";

import './verification.scss';

export default function Verification () {
    const token = useParams()

    axios.get(`/api/v1/login/activate/${token.uidb64}/${token.token}/`)
        .then(res => console.log(`then ${res}`))
        .catch(res => console.log(`catch ${res}`))

    return (
        <>
            <h2>Почта подтверждена</h2>
            <Redirect to="/account/edit/"/>
        </>
    )
}