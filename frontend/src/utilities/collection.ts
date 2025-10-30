import api from "../api"
import { accessToken } from "./constants"
import type { Card } from "./interfaces"

// Collection fetching
export const fetchCollection = async() => {

    try{
        const res = await api.get('/collection', {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        const collection = res.data.cards
        const numOfCollection = res.data.numOfCards
        
        return {collection: collection, numOfCollection: numOfCollection}
    }
    catch(err){
        console.error("Couldn't fetch collection")
        return {collection: [], numOfCollection: 0}
    }
}


// Collection adding
export const addToCollection = async(card: Card, count: number = 1) => {
    const card_id = card.card_id
    try{
        await api.post('/collection',{
            card_id: card_id,
            count: count
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

// Collection removing
export const removeFromCollection = async(card: Card, count: number = 1) => {
    const card_id = card.card_id
    try{
        await api.delete('/collection',{
            headers:{
                Authorization: `Bearer ${accessToken.value}`
            },
            data: {
                card_id: card_id,
                count: count
            }
        })
        return {'msg': 'Success'}
    }
    catch(err){
        console.error(err)
    }
}