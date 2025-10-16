import api from "../api"
import { payload } from "./constants"
import { refreshToken } from "./userAuthentification"

//--------------------------------
// Fetch all functions
//--------------------------------


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


//---------------------------
// Queries
//---------------------------

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

