import type { CredentialResponse } from "vue3-google-signin"
import api from "../api"
import { user, accessToken } from "./constants"

export const googleAuthentificationSuccess = async(response: CredentialResponse) => {
    try{
        console.log('Google respone: ', response)
        const res = await api.post('/auth-google',
                                    {credential: response.credential},
                                    {withCredentials: true})
        user.value = res.data.user
        accessToken.value = res.data.access_token
        return 'Success'
    }
    catch (err){
        console.error(err)
    }
}