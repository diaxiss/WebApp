import axios, { Axios } from "axios";
import { accessToken, refreshToken } from "./utilities/userAuthentification";


const api: Axios = axios.create({
    baseURL: "http://127.0.0.1:8000"
})

api.interceptors.response.use(response => {
    return response
}, async error => {
    const request = error.config
    request._retry = true
    if (error.response.status === 401){
        await refreshToken()
    }
    else{
        return
    }
    request.headers['Authorization'] = `Bearer ${accessToken.value}`
    return api.request(request);
})

export default api