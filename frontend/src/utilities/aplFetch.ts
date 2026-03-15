import api from "../api"
import { router } from "../main"
import { accessToken } from "./constants"
import type { SearchPayload, User } from "./interfaces"

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
export const fetchAllCards = async(payload: SearchPayload) => {

    try{
        const res = await api.post('/card', {
                limit: payload.limit,
                offset: payload.offset},
            {headers: {
                Authorization: `Bearer ${accessToken.value}`
            }})
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
export const queryCards = async(payload: SearchPayload) => {
    try{
        const res = await api.post('/search', payload, {
            headers:{
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        return {'cards': res.data.data,
                'numOfCards': res.data.numOfCards
        }
    }
    catch(err){
        console.error(err)
        return null
    }
}

export const fetchAllUsers = async() => {
    try{
        const res = await api.get('/users')
        console.log(res.data)
        return res.data.users as User[]
    }catch(err){
        console.error(err)
        return []
    }
}

export const fetchUser = async(user_id: string) => {
    try{
        const res = await api.get(`/user/${user_id || ''}`, {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        console.log(res.data)
        const picture = `http://localhost:8000/user_images/${res.data.picture}`
        return {'picture': picture, 'profile_user_name': res.data.name}
    }
    catch(err){
        router.push('/')
        console.error(err)
    }
}
