<script setup lang='ts'>

import '../styles/SearchForm.css'

import { payload } from '../utilities/constants.ts';
import { useCardSearch } from '../composables/useCardSearch.ts';
import { useCardMeta } from '../composables/useCardMeta.ts';



const {fetchQuery, setLimit} = useCardSearch()
const {allRarities, allSets, allIllustrators} = useCardMeta()

//------------------------------
// Functions to handle submits
//------------------------------

</script>


<template>
    <form class="submit-form" @submit.prevent="fetchQuery">

        <label for="card_name">Name: </label>
        <input placeholder = "Name..." id="card_name" v-model="payload.name">


        <label for="illustrator">Illustrator: </label>
        <select id="set" v-model="payload.illustrator">
            <option @select="payload.illustrator = ''"> </option>
            <option v-for="illustrator in allIllustrators" :value=illustrator>{{illustrator}}</option>
        </select>


        <label for="rarity">Rarity: </label>
        <select id="rarity" v-model="payload.rarity">
            <option @select="payload.rarity = ''"> </option>
            <option v-for="rarity in allRarities" :value=rarity>{{rarity}}</option>
         </select>


        <label for="set">Set: </label>
        <select id="set" v-model="payload.card_set">
            <option @select="payload.card_set = ''"> </option>
            <option v-for="set in allSets" :value=set>{{set}}</option>
        </select>


        <label for="card_id">Card id: </label>
        <input placeholder = "Card id..." id="card_id" type="text" v-model="payload.card_id">


        <label id="release_date">Release date: </label>

        <div class="release-date">
            <input placeholder = "Release date..." aria-labelledby="release_date" id="release_date_from" type="date" v-model="payload.release_date_from" :max="(payload.release_date_to as string)">
            <span> - </span>
            <input placeholder = "Release date..." aria-labelledby="release_date" id="release_date_to" type="date" v-model="payload.release_date_to" :min="(payload.release_date_from as string)">
        </div>


        <div>
            <label for="limit">Limit per page:</label>
            <select id="limit" v-model="payload.limit" 
                    @change="setLimit">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
            </select>
        </div>
        <button type="submit">Submit</button>
    </form>
</template>