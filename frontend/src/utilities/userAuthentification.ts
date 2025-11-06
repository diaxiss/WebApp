import type { CredentialResponse } from "vue3-google-signin"
import api from "../api"
import { userPicture, userName, accessToken, collection, wishlist, isLoggedOut, userId } from "./constants"
import { fetchCollection } from "./collection"
import { fetchWishlist } from "./wishlist"
import { router } from "../main"

function setToken(token: string){
    accessToken.value = token
    localStorage.setItem('accessToken', token)
}

export const handleLogout = async() => {
    isLoggedOut.value = true
    try{
        await api.post('/logout',{},{
            withCredentials: true
        })
    } catch(err){
        console.error('Logout API failed', err)
    }

    ['accessToken', 'user', 'image'].forEach
    (key => localStorage.removeItem(key))

    accessToken.value = null
    userName.value = null
    userPicture.value = null
    collection.value = []
    wishlist.value = []

    router.push('/')

}

export const googleAuthentificationSuccess = async(response: CredentialResponse) => {
    try{
        const res = await api.post('/auth-google',
                                    {credential: response.credential},
                                    {withCredentials: true})
        userName.value = res.data.user.name
        userId.value = res.data.user.id
        userPicture.value = res.data.user.picture
        localStorage.setItem('user', userName.value || '')
        localStorage.setItem('id', userId.value || '')
        localStorage.setItem('image', userPicture.value || '')
        setToken(res.data.access_token)
        
        const collectionRes = await fetchCollection()
        collection.value = collectionRes.collection
        const wishlistRes = await fetchWishlist()
        wishlist.value = wishlistRes.wishlist
        return 'Success'
    }
    catch (err){
        console.error('Authentification failed', err)
    }
}

export const refreshToken = async() => {
    try{
        const response = await api.post('/refresh-token',
            {},
            {withCredentials: true}
        )
        accessToken.value = response.data.access_token
        localStorage.setItem('accessToken', response.data.access_token)
    }catch (err){
        console.error('Refreshing access token failed', err)
        throw err
    }
}