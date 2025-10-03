import axios, { Axios } from "axios";


const api: Axios = axios.create({
    baseURL: "http://127.0.0.1:8000"
})

export default api