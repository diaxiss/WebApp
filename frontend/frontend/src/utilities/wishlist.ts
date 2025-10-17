import api from "../api"
import { accessToken } from "./constants"
import type { Card } from "./interfaces"

// Wishlist fetching
export const fetchWishlist = async() => {

    try{
        const res = await api.get('/wishlist', {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        const wishlist = res.data.cards
        const numOfWishlist = res.data.numOfCards
        return {wishlist: wishlist, numOfWishlist: numOfWishlist}
    }
    catch(err){
        console.error(err)
        return {wishlist: [], numOfWishlist: 0}
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