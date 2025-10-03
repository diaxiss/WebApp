<script setup lang="ts">
import type { Card } from './Interfaces.vue'
import placeholder_image from '../assets/placeholder.png'
import '../styles/QueryResults.css'
import { currentPage, numOfPages } from '../utilities/usePagination';

defineProps<{
  cards: Card[]
}>()

const emits = defineEmits<{
    (e: 'load'): void
}>()
// Function to fetch local images for cards
function fetchImage(image: string | null){

    if (image === null){
        return placeholder_image
    }
    return `http://localhost:8000/images/${image}`
}
</script>

<template>
    <div>    

        <div class="query-container">

            <div class="query-item-container" v-for="result in cards" :key="result.card_id">

                <img class='card-image' :src="fetchImage(result.image)">
                <p>{{ result.card_set }}</p>
                <p>{{ result.release_date }}</p>
                <!-- <p>{{ result.rarity }}</p> -->

            </div>

        </div>
        
        <button v-show="currentPage < numOfPages"type="button" @click="$emit('load')">Load more</button>

    </div>
</template>