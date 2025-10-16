<style src="../styles/Home.css"></style>
<script setup lang='ts'>

import SearchForm from '../components/SearchForm.vue';
import PageHeader from '../components/PageHeader.vue';
import PageIndicator from '../components/PageIndicator.vue';
import CardContainer from '../components/CardContainer.vue';

import type { Card } from '../utilities/interfaces';

import { onMounted, ref, type Ref} from 'vue'
import { payload, numOfPages, numOfCards, currentPage, collection, wishlist } from '../utilities/constants';
import { fetchAllCards, fetchAllIllustrators, fetchAllRarities, fetchAllSetsInfo, queryCards } from '../utilities/aplFetch';
import { accessToken } from '../utilities/constants';
import { addToWishlist, removeFromWishlist } from '../utilities/wishlist';
import { addToCollection, removeFromCollection } from '../utilities/collection';



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
async function handleAddToCollection(card: Card){

    const wishlistIndex = wishlist.value.findIndex(testCard => {
        return testCard.card_id === card.card_id
    })
    if (wishlistIndex !== -1){
        wishlist.value.splice(wishlistIndex, 1)
    }
    const index = collection.value.findIndex(testCard => {
            return testCard.card_id === card.card_id
        })
    if (index !== -1){
        if (collection.value[index]?.count){
            collection.value[index].count += 1
        }
    }else{
        collection.value.push({...card, count: 1})
    }
    const res = await addToCollection(card)
    const res2 = await removeFromWishlist(card)
    if (res?.msg == 'Success' && res2?.msg == 'Success') return
    
    else if (collection.value[index]?.count){
        if (collection.value[index].count == 1){
            collection.value.splice(index,1)
        }
        else{
            collection.value[index].count -= 1
        }
        if (wishlistIndex !== -1){
            wishlist.value.splice(wishlistIndex,0, card)
        }
    }
}

async function handleRemoveFromCollection(card: Card){

    const index = collection.value.findIndex(testCard => {
            return testCard.card_id === card.card_id
        })

    if (index === -1) return

    const card_copy = {...collection.value[index]} as Card

    if (!collection.value[index] || !collection.value[index].count) return

    if (collection.value[index].count > 1){
        collection.value[index].count -= 1
    }
    else{
        collection.value.splice(index, 1)
    }
    
    const res = await removeFromCollection(card)

    if (res?.msg == 'Success') return
    const rollbackIndex = collection.value.findIndex(
        testCard => testCard.card_id === card.card_id
    )
    if(rollbackIndex === -1){
        collection.value.push(card_copy)
    }
    else {
        collection.value[rollbackIndex] = {...card_copy}
    }
}

async function handleRemoveFromWishlist(card: Card){
    const index = wishlist.value.findIndex(testCard => {
            return testCard.card_id === card.card_id
        })
    const card_copy = wishlist.value[index] as Card

    wishlist.value.splice(index,1)

    const res = await removeFromWishlist(card)
    if (res?.msg == 'Success') return

    else wishlist.value.splice(index, 0, card_copy)
}

async function handleAddToWishlist(card: Card){
    wishlist.value.push(card)
    const res = await addToWishlist(card)
    if (res?.msg == 'Success') return

    else wishlist.value.pop()
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

    <CardContainer
        :cards="loadedCards"
        :display-info="true"
        :extra-options="true"
        @wishlist-add="handleAddToWishlist"
        @wishlist-remove="handleRemoveFromWishlist"
        @collection-add="handleAddToCollection"
        @collection-remove="handleRemoveFromCollection"/>

    <PageIndicator
        @load="handleLoad"/>

</template>