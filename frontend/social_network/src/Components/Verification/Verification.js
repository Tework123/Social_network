import {useParams} from "react-router-dom";
import axios from "../../Api/axios";

export default function Verification () {
    const token = useParams()
    console.log(token.uidb64 + " " + token.token)

    axios.get(`/api/v1/login/activate/${token.uidb64}/${token.token}`)
        .then(res => console.log(`then ${res}`))
        .catch(res => console.log(`catch ${res}`))

    return (
        <div>Почта подтверждена</div>
    )
}