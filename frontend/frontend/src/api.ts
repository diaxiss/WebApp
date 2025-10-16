import axios, { Axios } from "axios";
import { handleLogout, refreshToken } from "./utilities/userAuthentification";
import { accessToken } from "./utilities/constants";


const api: Axios = axios.create({
    baseURL: "http://127.0.0.1:8000"
})

api.interceptors.response.use(response => {
    return response
}, async error => {

    const request = error.config
    if (axios.isAxiosError(error) && error.response?.status === 401 && !request._retry){
        request._retry = true
    
        try{
            await refreshToken()
            request.headers['Authorization'] = `Bearer ${accessToken.value}`
            return api.request(request);
        }catch (err){
            if (axios.isAxiosError(err)){
                if (err.response?.status === 422){
                    handleLogout()
                }
            }
            return Promise.reject(err)
        }
    }
    return Promise.reject(error)
})

export default api