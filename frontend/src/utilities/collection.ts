import api from "../api"
import { accessToken } from "./constants"
import type { Card } from "./interfaces"

// Collection fetching
export const fetchCollection = async(limit: number = 10, offset: number = 0, user_id?: string) => {

    try{
        const res = await api.get(`/collection/${user_id ? 'user/'+user_id : ''}`, {
            params: {
                limit: limit,
                offset: offset
            },
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        const collection = res.data.cards
        const collectionLength = res.data.length
        
        return [collection, collectionLength]
    }
    catch(err){
        console.error("Couldn't fetch collection")
        return [[], 0]
    }
}

// Collection adding
export const addToCollection = async(card: Card) => {
    const card_id = card.card_id
    try{
        await api.post(`/collection`,
            {card_id: card_id},
            {headers: {
                Authorization: `Bearer ${accessToken.value}`
            }}
        )
        return {'msg': 'Success'}
    }
    catch(err){
        console.error('Failed to add the card to your collection')
    }
}

// Collection removing
export const removeFromCollection = async(card: Card) => {
    const card_id = card.card_id
    try{
        await api.delete(`/collection/${card_id}`, {
            headers:{
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        return {'msg': 'Success'}
    }
    catch(err){
        console.error('Failed to remove the card from your collection')
    }
}