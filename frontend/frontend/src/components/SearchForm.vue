<script setup lang='ts'>
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
        <input placeholder = "Illustrator..." id="illustrator" list="card-illustrators" v-model="payload.illustrator">
        <datalist id="card-illustrators">
            <option v-for="illustrator in allIllustrators" :value=illustrator>{{illustrator}}</option>
        </datalist>


        <label for="rarity">Rarity: </label>
        <input placeholder = "Rarity..." id="rarity" list = 'card-rarities' v-model="payload.rarity">
        <datalist id="card-rarities">
            <option v-for="rarity in allRarities" :value=rarity>{{rarity}}</option>
        </datalist>


        <label for="set">Set: </label>
        <input placeholder = "Set..." id="set" type='text' list="card-sets" v-model="payload.card_set">
        <datalist id="card-sets">
            <option v-for="set in allSets" :value=set>{{set}}</option>
        </datalist>


        <label for="card_id">Card id: </label>
        <input placeholder = "Card id..." id="card_id" type="text" v-model="payload.card_id">


        <label id="release_date">Release date: </label>

        <div>
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
        <input type="submit">
    </form>
</template>