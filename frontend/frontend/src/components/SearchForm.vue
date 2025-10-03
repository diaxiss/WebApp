<script setup lang='ts'>
import type { SearchPayload } from './Interfaces.vue';
import { payload } from '../utilities/usePagination.ts';


//-----------------------
// Props passed through
//----------------------

defineProps<{
  allRarities: String[]
  allSets: String[]
  allIllustrators: String[]
}>()


//----------------
// Define emits
//----------------

const emits = defineEmits<{
    (e: 'submit'): void
    (f: 'change'): void
}>()


//--------------------
// Search variables
//--------------------


//------------------------------
// Functions to handle submits
//------------------------------

// Handles form submit
const handleSubmit = async() => {

    (Object.keys(payload) as Array<keyof SearchPayload>).forEach(key => {
        if (payload[key] == null || payload[key] == "") delete payload[key];
    });

    payload.offset = 0
    emits('submit')
}

// Handles items per page change

</script>


<template>
    <form class="submit-form" @submit.prevent="handleSubmit">

        <label for="name">Name: </label>
        <input placeholder = "Name..." name="name" v-model="payload.name">


        <label for="name">Illustrator: </label>
        <input placeholder = "Illustrator..." name="illustrator" list="card-illustrators" v-model="payload.illustrator">
        <datalist id="card-illustrators">
            <option v-for="illustrator in allIllustrators" :value=illustrator>{{illustrator}}</option>
        </datalist>


        <label for="rarity">Rarity: </label>
        <input placeholder = "Rarity..." name="rarity" list = 'card-rarities' v-model="payload.rarity">
        <datalist id="card-rarities">
            <option v-for="rarity in allRarities" :value=rarity>{{rarity}}</option>
        </datalist>


        <label for="set">Set: </label>
        <input placeholder = "Set..." name="set" type='text' list="card-sets" v-model="payload.card_set">
        <datalist id="card-sets">
            <option v-for="set in allSets" :value=set>{{set}}</option>
        </datalist>


        <label for="card_id">Card id: </label>
        <input placeholder = "Card id..." name="card_id" type="text" v-model="payload.card_id">

        <label for="release_date">Release date: </label>
        <input placeholder = "Release date..." name="release_date" type="text" v-model="payload.release_date">

        <div>
            <label>Limit per page:</label>
            <select v-model="payload.limit" 
                    @change="{$emit('change'); payload.offset = 0}">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
            </select>
        </div>
        <input type="submit">
    </form>
</template>