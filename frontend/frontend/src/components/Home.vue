<style src="../styles/Home.css"></style>
<script setup lang='ts'>

import api from '../api';
import placeholder_image from '../assets/placeholder.png'
import SearchForm from './SearchForm.vue'
import PageHeader from './PageHeader.vue';

import type { Card } from './Interfaces.vue';

import { ref, type Ref} from 'vue'
import { payload } from '../utilities/usePagination';


//---------------------
// Reactive States
//---------------------

// API result variables
let allSets: Ref<String[]> = ref<String[]>([])
let allRarities: Ref<String[]> = ref<String[]>([])
let allIllustrators: Ref<String[]> = ref<String[]>([])

let queryResult: Ref<Card[]> = ref<Card[]>([])
let loadedCards: Ref<Card[]> = ref<Card[]>([])

const numOfCards: Ref<number> = ref<number>(0)
const numOfPages: Ref<number> = ref<number>(-1)

//-------------------------
// API functions on mount
//-------------------------

// function to fetch all cards
const fetchAllCards = async() => {

    try{
        api
            .post('/cards', {
                limit: payload.limit,
                offset: payload.offset})
            .then((res) => res.data)
            .then((data) => {
                loadedCards.value = [...loadedCards.value, ...data.cards as Card[]]
                numOfCards.value = data.numOfCards
                numOfPages.value = Math.ceil(numOfCards.value/payload.limit)
                console.log(loadedCards)
            })
    }
    catch(err){
        console.error(err)
    }
}

// Function to fetch all rarities
const fetchAllRarities = async() => {

    try{
        api
            .get('/sets')
            .then((res) => res.data)
            .then((data) => {
                allSets = data.sets
            })
    }
    catch(err){
        console.error(err)
    }
}

// Function to fetch all sets
const fetchAllSets = async() => {

    try{
        api
            .get('/rarities')
            .then((res) => res.data)
            .then((data) => {
                allRarities = data.rarities
            })
    }
    catch(err){
        console.error(err)
    }
}

// Function to fetch all illustrators
const fetchAllIllustrators = async() => {

    try{
        api
            .get('/illustrators')
            .then((res) => res.data)
            .then((data) => {
                allIllustrators = data.illustrators
            })
    }
    catch(err){
        console.error(err)
    }
}


//------------------
// Query functions
//------------------

// Function to fetch images for cards
function fetchImage(image: string | null){

    if (image === null){
        return placeholder_image
    }
    return `http://localhost:8000/images/${image}`
}

// API call to handle form submit
const handleSearch = async() =>{


    console.log(`Limit: ${payload.limit}, Offset: ${payload.offset}`)
    console.log(payload)
    try{
        const res = await api.post('/search', payload)
        queryResult.value = [...queryResult.value, ...res.data.data as Card[]]
        console.log(queryResult)
    }
    catch(err){
        console.error(err)
    }
}

const handleSeachSubmit = () => {
    queryResult.value = []
    handleSearch()
}

// API call for items after item per page change
const handlePageChange = () =>{

    //Reset all values
    loadedCards.value = []

    payload.offset = 0

    // Fetch either all cards, or repeat payload request
    if (queryResult.value.length > 0){
        queryResult.value = []
        handleSeachSubmit()
    }
    else {
        fetchAllCards();
    }
}


//----------------------------------
// Run necessary fetch functions
//----------------------------------

fetchAllSets()
fetchAllRarities()
fetchAllIllustrators()
fetchAllCards()
</script>


<!--               -->
<!-- HTML Template -->
<!--               -->

<template>

    <PageHeader />

    <SearchForm
        :allSets = "allSets"
        :allRarities = "allRarities"
        :allIllustrators = "allIllustrators"
        :offset = "payload.offset"
        :limit = "payload.limit"
        @submit="handleSeachSubmit"
        @change="handlePageChange"
    />

    <!-- Loaded Cards -->
    <div v-if=" queryResult.length == 0">    

        <div class="query-container">

            <div class="query-item-container" v-for="result in loadedCards" :key="result.card_id">

                <img class='card-image' :src="fetchImage(result.image)">
                <p>{{result.name}}</p>
                <p>{{ result.card_set }}</p>

            </div>

        </div>

        <button type="button" @click="{payload.offset += payload.limit; fetchAllCards()}">Load more</button>

    </div>

    <!-- Queried cards -->
    <div v-else-if="queryResult.length > 0">
        

        <div  class="query-container">

            <div class="query-item-container" v-for="result in queryResult" :key="result.card_id">

                <img class='card-image' :src="fetchImage(result.image)">
                <p>{{ result.card_set }}</p>
                <p>{{ result.release_date }}</p>
                <p>{{ result.rarity }}</p>

            </div>

        </div>

        <button type="button" @click="{payload.offset += payload.limit; handleSearch()}">Load more</button>
    
    </div>


</template>