import axios, { Axios } from "axios";
import { handleLogout, refreshToken } from "./utilities/userAuthentification";
import { accessToken, isLoggedOut } from "./utilities/constants";

console.log(import.meta.env.VITE_API_URL)
const api: Axios = axios.create({
    // baseURL: import.meta.env.BASE_URL
    baseURL: import.meta.env.VITE_API_URL
})

api.interceptors.response.use(response => {
    return response
}, async error => {

    const request = error.config

    if (axios.isAxiosError(error) &&
        error.response?.status === 401 &&
        !request._retry &&
        !request.url?.includes('/refresh') &&
        !isLoggedOut.value){
        request._retry = true
    
        try{
            await refreshToken()
            request.headers['Authorization'] = `Bearer ${accessToken.value}`
            return api.request(request);
        }catch (err){
            handleLogout()
            return Promise.reject(err)
        }
    }
    return Promise.reject(error)
})

export default api