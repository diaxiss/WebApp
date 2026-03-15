<script setup lang='ts'>

import LimitSelect from './LimitSelect.vue';
import '../styles/SearchForm.css'

import { useCardSearch } from '../composables/useCardSearch.ts';
import { useCardMeta } from '../composables/useCardMeta.ts';
import { usePayloadStore } from '../stores/payloadStore.ts';
import type { Card } from '../utilities/interfaces.ts';



const {fetchQuery} = useCardSearch()
const {allRarities, allSets, allIllustrators} = useCardMeta()

const emits = defineEmits(['submit'])

const store = usePayloadStore()

//------------------------------
// Functions to handle submits
//------------------------------

const changeLimit = async(limit: number) => {
    store.payload.limit = limit
    emits('submit', await fetchQuery({...store.payload}) as [Card[], number])
}

const handleSubmit = async() => {
    emits('submit', await fetchQuery({...store.payload}) as [Card[], number])
}

</script>


<template>
    <form class="submit-form" @submit.prevent="handleSubmit">

        <label for="card_name">Name: </label>
        <input placeholder = "Name..." id="card_name" v-model="store.payload.name">


        <label for="illustrator">Illustrator: </label>
        <select id="set" v-model="store.payload.illustrator">
            <option @select="store.payload.illustrator = ''"> </option>
            <option v-for="illustrator in allIllustrators" :value=illustrator>{{illustrator}}</option>
        </select>


        <label for="rarity">Rarity: </label>
        <select id="rarity" v-model="store.payload.rarity">
            <option @select="store.payload.rarity = ''"> </option>
            <option v-for="rarity in allRarities" :value=rarity>{{rarity}}</option>
         </select>


        <label for="set">Set: </label>
        <select id="set" v-model="store.payload.card_set">
            <option @select="store.payload.card_set = ''"> </option>
            <option v-for="set in allSets" :value=set>{{set}}</option>
        </select>


        <label for="card_id">Card id: </label>
        <input placeholder = "Card id..." id="card_id" type="text" v-model="store.payload.card_id">


        <label id="release_date">Release date: </label>

        <div class="release-date">
            <input placeholder = "Release date..." aria-labelledby="release_date" id="release_date_from" type="date" v-model="store.payload.release_date_from" :max="(store.payload.release_date_to as string)">
            <span> - </span>
            <input placeholder = "Release date..." aria-labelledby="release_date" id="release_date_to" type="date" v-model="store.payload.release_date_to" :min="(store.payload.release_date_from as string)">
        </div>


        <LimitSelect @change="changeLimit"/>
        <button type="submit">Submit</button>
    </form>
</template>