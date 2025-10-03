<style src="../styles/Home.css"></style>
<script setup lang='ts'>

import api from '../api';
import SearchForm from './SearchForm.vue'
import PageHeader from './PageHeader.vue';
import QueryResults from './QueryResults.vue';

import type { Card } from './Interfaces.vue';

import { ref, type Ref} from 'vue'
import { payload, numOfPages, numOfCards, currentPage } from '../utilities/usePagination';


//---------------------
// Reactive States
//---------------------

// API result variables
let allSets: Ref<String[]> = ref<String[]>([])
let allRarities: Ref<String[]> = ref<String[]>([])
let allIllustrators: Ref<String[]> = ref<String[]>([])

let queriedCards: Ref<Card[]> = ref<Card[]>([])
let loadedCards: Ref<Card[]> = ref<Card[]>([])

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
        const res = await api.get('/illustrators')
        allIllustrators = res.data.illustrators
    }
    catch(err){
        console.error(err)
    }
}


//----------------------------------
// Run necessary API functions
//----------------------------------

fetchAllSets()
fetchAllRarities()
fetchAllIllustrators()
fetchAllCards()


//------------------
// Query functions
//------------------

// API call to handle form submit

const queryCards = async() =>{
    try{
        const res = await api.post('/search', payload)
        //queriedCards.value = [...queriedCards.value, ...res.data.data as Card[]]
        queriedCards.value = res.data.data as Card[]
        numOfCards.value = res.data.numOfCards
        numOfPages.value = Math.ceil(numOfCards.value / payload.limit)

    }
    catch(err){
        console.error(err)
    }
}


//----------------------------
// Event handler functions
//----------------------------

// Function to handle SearchForm form submit
const handleSeachSubmit = () => {
    queriedCards.value = []
    currentPage.value = 1
    queryCards()
}

// Function to handle SearchForm limit change
const handlePageChange = () =>{

    // Reset all values
    loadedCards.value = []

    payload.offset = 0

    // Fetch either all cards, or repeat payload request
    if (queriedCards.value.length > 0){
        queriedCards.value = []
        handleSeachSubmit()
    }
    else {
        fetchAllCards();
    }
}

// Function to handle Load More for queried cards 
const handleLoadMoreQueryCards = () => {
    
    if (currentPage.value >= numOfPages.value) return

    payload.offset = payload.limit*currentPage.value;

    queryCards();

    currentPage.value++;
    
}

// Function to handle Load More for all cards
const handleLoadMoreAllCards = () => {
    payload.offset += payload.limit
    fetchAllCards()
}

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
        @submit="handleSeachSubmit"
        @change="handlePageChange"
    />

    <!-- Loaded Cards -->
    <QueryResults
        v-if=" queriedCards.length == 0" 
        :cards="loadedCards" 
        @load="handleLoadMoreAllCards"/>

    <QueryResults 
        v-else-if="queriedCards.length > 0"
        :cards="queriedCards"
        @load="handleLoadMoreQueryCards"/>


</template>