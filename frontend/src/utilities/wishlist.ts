import api from "../api"
import { accessToken } from "./constants"
import type { Card } from "./interfaces"

// Wishlist fetching
export const fetchWishlist = async(user_id?: string) => {

    try{
        const res = await api.get(`/wishlist/${user_id || ''}`, {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        const wishlist = res.data.cards
        const numOfWishlist = res.data.numOfCards
        return {wishlist: wishlist, numOfWishlist: numOfWishlist}
    }
    catch(err){
        console.error("Couldn't fetch wishlist")
        return {wishlist: [], numOfWishlist: 0}
    }
}



export const fetchWishlistSummary = async(user_id: string) => {

    try{
        const res = await api.get(`/wishlist/summary/${user_id || ''}`, {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        return res.data.cards
    }
    catch(err){
        console.error(err)
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
        await api.delete('/wishlist', {
            headers:{
                Authorization: `Bearer ${accessToken.value}`
            },
            data: {
                card_id: card_id
            }
        })
        return {'msg': 'Success'}
    }
    catch(err){
        console.error(err)
    }
}