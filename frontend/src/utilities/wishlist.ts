import api from "../api"
import { accessToken } from "./constants"
import type { Card } from "./interfaces"

// Wishlist fetching
export const fetchWishlist = async(limit: number = 10, offset: number = 0, user_id?: string) => {

    try{
        const res = await api.get(`/wishlist/${user_id ? 'user/'+user_id : ''}`, {
            params: {
                limit: limit,
                offset: offset
            },
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        const wishlist = res.data.cards
        const wishlistLength = res.data['length']
        return [wishlist, wishlistLength]
    }
    catch(err){
        console.error("Couldn't fetch wishlist")
        return [[], 0]
    }
}

//Wishlist adding
export const addToWishlist = async(card: Card) => {

    const card_id = card.card_id
    try{
        await api.post('/wishlist',{
            card_id: card_id
        }, {headers: {
            Authorization: `Bearer ${accessToken.value}`
        }
        })
        return {'msg': 'Success'}
    }
    catch(err){
        console.error(err)
    }
}

// Wishlist removing
export const removeFromWishlist = async(card: Card) => {
    const card_id = card.card_id
    try{
        await api.delete(`/wishlist/${card_id}`, {
            headers:{
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        return {'msg': 'Success'}
    }
    catch(err){
        console.error(err)
    }
}