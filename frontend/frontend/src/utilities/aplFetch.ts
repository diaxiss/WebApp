import api from "../api"
import placeholder_image from '../assets/placeholder.png'
import { payload } from "./constants"

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
export async function fetchImage(image: string | null){

    if (image === null){
        return placeholder_image
    }
    // return `http://localhost:8000/images/${image}`
    try{
        await api.get(`/images/${image}`)
        return `http://localhost:8000/images/${image}`
    }
    catch(err){
        return placeholder_image
    }
}

