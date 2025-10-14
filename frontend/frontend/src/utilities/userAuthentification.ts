import type { CredentialResponse } from "vue3-google-signin"
import api from "../api"
import { ref } from "vue"
import { userPicture, userName } from "./constants"
import { router } from "../main"

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
    router.push('/')

}

export const googleAuthentificationSuccess = async(response: CredentialResponse) => {
    try{
        console.log('Google respone: ', response)
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