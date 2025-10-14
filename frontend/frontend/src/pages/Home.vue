<style src="../styles/Home.css"></style>
<script setup lang='ts'>

import SearchForm from '../components/SearchForm.vue';
import PageHeader from '../components/PageHeader.vue';
import PageIndicator from '../components/PageIndicator.vue';
import CardContainer from '../components/CardContainer.vue';

import type { Card } from '../utilities/interfaces';

import { onMounted, ref, type Ref} from 'vue'
import { payload, numOfPages, numOfCards, currentPage } from '../utilities/constants';
import { fetchAllCards, fetchAllIllustrators, fetchAllRarities, fetchAllSetsInfo, queryCards } from '../utilities/aplFetch';
import { accessToken } from '../utilities/userAuthentification';



//---------------------
// Reactive States
//---------------------

// API result variables
const allSets: Ref<String[]> = ref<String[]>([]);
const allRarities: Ref<String[]> = ref<String[]>([]);
const allIllustrators: Ref<String[]> = ref<String[]>([]);

const loadedCards: Ref<Card[]> = ref<Card[]>([])
let _queried: boolean = false;


//-------------------------
// API functions on mount
//-------------------------
onMounted(async () => {

    allSets.value = await fetchAllSetsInfo()
    allRarities.value = await fetchAllRarities()
    allIllustrators.value = await fetchAllIllustrators()

    handleFetchAllCards()

})


//------------------
// Query functions
//------------------

// API call to handle form submit
const handleQueryCards = async() =>{
    _queried = true
    const res = await queryCards()
    loadedCards.value = res?.cards
    numOfCards.value = res?.numOfCards
    numOfPages.value = res?.numOfPages ?? 1


}

//----------------------------
// Event handler functions
//----------------------------

// Handler function to fetch all cards
const handleFetchAllCards = async() => {

    _queried = false
    const cards: any = await fetchAllCards()
    loadedCards.value = cards.cards as Card[]
    numOfCards.value = cards.numOfCards as number
    numOfPages.value = Math.ceil(numOfCards.value/payload.limit)
    console.log(loadedCards.value)
}


// Function to handle SearchForm form submit
const handleSeachSubmit = () => {
    currentPage.value = 1
    handleQueryCards()
}

// Function to handle SearchForm limit change
const handlePageChange = () =>{

    payload.offset = 0
    console.log(accessToken.value)
    // Fetch either all cards, or repeat payload request
    if (_queried) handleSeachSubmit();
    else handleFetchAllCards();
}


// Handler for show all cards button
const showAllCards = () => {
    loadedCards.value = []
    payload.offset = 0
    currentPage.value = 1
    handleFetchAllCards()
}


// Handler for load more button
const handleLoad = (page: number) => {
    
    payload.offset = payload.limit*(page-1);
    currentPage.value = (payload.offset / payload.limit) + 1

    if (_queried) handleQueryCards();
    else handleFetchAllCards();
    
}

</script>


<template>

    <PageHeader />

    <SearchForm
        :allSets = "allSets"
        :allRarities = "allRarities"
        :allIllustrators = "allIllustrators"
        @submit="handleSeachSubmit"
        @change="handlePageChange"
    />
    <button @click="showAllCards">All cards</button>

    <!-- <QueryResultsCards
        :cards="loadedCards"
        @load="handleLoad"/> -->
    <CardContainer
        :cards="loadedCards"
        :display-info="true"
        :extra-options="true"/>        

    <PageIndicator
        @load="handleLoad"/>

</template>