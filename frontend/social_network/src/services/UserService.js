import axios from "../api/axios";

const _apiBase = 'http://127.0.0.1:8000/api/v1/'
export const getUser = async (id) => {
    const res = await axios.get(`${_apiBase}account/im/${id}/`)
    return _transformUser(res.data)
}

const _transformUser = (user) => {
    return {
        firstName: user.first_name,
        lastName: user.last_name,
        phone: user.phone,
        email: user.email,
        city: user.city,
        aboutMe: user.about_me,
        dateOfBirth: user.date_of_birth,
        lifestyle: user.lifestyle,
        interest: user.interest,
        avatar: user.avatar,
        dateJoined: user.date_joined,
        dateLastVisit: user.date_last_visit,
        dateLastPasswordReset: user.date_last_password_reset,
        education: [],
        work: []
    }
}