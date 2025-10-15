import api from "../api"
import placeholder_image from '../assets/placeholder.png'
import { payload } from "./constants"
import { accessToken, refreshToken } from "./userAuthentification"


// Function to fetch all rarities
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

// Function to fetch all cards
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

// Function to fetch all sets
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

// Function to fetch all sets short info
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

// Function to handle card queries
export const queryCards = async() => {
    try{
        refreshToken()
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
        console.error(err)
        return {collection: [], numOfCollection: 0}
    }
}

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
export const handleAddToWishlist = async(card_id: string) => {

    try{
        await api.post('/wishlist',{
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

// Wishlist removing
export const handleRemoveFromWishlist = async(card_id: string) => {
    try{
        await api.delete('/wishlist', {
            headers:{
                Authorization: `Bearer ${accessToken.value}`
            },
            data: {
                card_id: card_id
            }
        })
    }
    catch(err){
        console.error(err)
    }
}


// Collection adding
export const handleAddToCollection = async(card_id: string, count: number) => {
    try{
        await api.post('/collection',{
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

// Collection removing
export const handleRemoveFromCollection = async(card_id: string, count: number = 1) => {
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
    }
    catch(err){
        console.error(err)
    }
}