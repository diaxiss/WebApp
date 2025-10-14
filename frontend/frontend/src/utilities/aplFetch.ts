import api from "../api"
import placeholder_image from '../assets/placeholder.png'
import { payload } from "./constants"
import { accessToken } from "./userAuthentification"

// Function to fetch all rarities
export const fetchAllSetsInfo = async() => {

    try{
        const res = await api.get('/sets/info')
        return res.data.sets
    }
    catch(err){
        console.error(err)
        return null
    }
}

// Function to fetch all sets
export const fetchAllRarities = async() => {

    try{
        const res = await api.get('/rarities/info')
                return res.data.rarities
    }
    catch(err){
        console.error(err)
        return null
    }
}

// Function to fetch all illustrators
export const fetchAllIllustrators = async() => {

    try{
        const res = await api.get('/illustrators/info')
        return res.data.illustrators
    }
    catch(err){
        console.error(err)
        return null
    }
}

export const fetchAllCards = async() => {

    try{
        const res = await api.post('/cards', {
                limit: payload.limit,
                offset: payload.offset})
        return {'cards': res.data.cards, 'numOfCards': res.data.numOfCards}
    }
    catch(err){
        console.error(err)
        return null
    }
}

export async function fetchAllSets(){
    try{
        const res = await api.get('/sets')
        return res.data.sets
    }
    catch(err){
        console.error(err)
        return null
    }
}

export const queryCards = async() => {
    try{
        const res = await api.post('/search', payload)
        return {'cards': res.data.data,
                'numOfCards': res.data.numOfCards,
                'numOfPages':  Math.ceil(res.data.numOfCards / payload.limit)
        }
    }
    catch(err){
        console.error(err)
        return null
    }
}

// Function to fetch local images for cards
export async function fetchImage(image: string | null, folder: string){

    if (image === null){
        return placeholder_image
    }
    try{
        await api.head(`/${folder}/${image}`)
        return `http://localhost:8000/${folder}/${image}`
    }
    catch(err){
        return placeholder_image
    }
}


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
        console.error(err)
        return {collection: [], numOfCollection: 0}
    }
}

export const fetchWishlist = async() => {

    try{
        const res = await api.get('/wishlist', {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        const wishlist = res.data.cards
        const numOfWishlist = res.data.numOfCards
        console.log(res.data)
        return {wishlist: wishlist, numOfWishlist: numOfWishlist}
    }
    catch(err){
        console.error(err)
        return {wishlist: [], numOfWishlist: 0}
    }
}

export const handleAddToWishlist = async(card_id: string) => {
    console.log(card_id)
    try{
        const res = await api.post('/wishlist/add',{
            card_id: card_id
        }, {headers: {
            Authorization: `Bearer ${accessToken.value}`
        }
        })
    }
    catch(err){
        console.error(err)
    }
}


export const handleAddToCollection = async(card_id: string, count: number) => {
    try{
        console.log(card_id, count)
        const res = await api.post('/collection/add',{
            card_id: card_id,
            count: count
        }, {headers: {
            Authorization: `Bearer ${accessToken.value}`
        }
        })
    }
    catch(err){
        console.error(err)
    }
}


