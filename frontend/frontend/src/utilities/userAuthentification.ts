import type { CredentialResponse } from "vue3-google-signin"
import api from "../api"
import { ref } from "vue"
import { userPicture, userName } from "./constants"

export const accessToken = ref(localStorage.getItem('accessToken'))

function setToken(token: string){
    accessToken.value = token
    localStorage.setItem('accessToken', token)
}

export const handleLogout = async() => {
    localStorage.removeItem('accessToken')
    accessToken.value = null
    localStorage.removeItem('user')
    userName.value = null
    localStorage.removeItem('image')
    userPicture.value = null
    await api.post('/logout')
}

export const googleAuthentificationSuccess = async(response: CredentialResponse) => {
    try{
        const res = await api.post('/auth-google',
                                    {credential: response.credential},
                                    {withCredentials: true})
        userName.value = res.data.user.name
        userPicture.value = res.data.user.picture
        localStorage.setItem('user', userName.value || 'what')
        localStorage.setItem('image', userPicture.value || 'huh')
        setToken(res.data.access_token)
        return 'Success'
    }
    catch (err){
        console.error(err)
    }
}

export const refreshToken = async() => {
    const response = await api.post('/refresh-token',
        {},
        {withCredentials: true}
    )
    accessToken.value = response.data.access_token
    localStorage.setItem('accessToken', response.data.access_token)
}