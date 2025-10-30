<script setup lang="ts">

import '../styles/Sets.css'

import { onMounted, ref, type Ref } from 'vue';

import PageHeader from '../components/PageHeader.vue';

import type { SetCard } from '../utilities/interfaces';

import { fetchAllSets } from '../utilities/aplFetch';

import { router } from '../main';
import { API_URL } from '../utilities/constants';


const sets: Ref<SetCard[]> = ref<SetCard[]>([])


onMounted(async() => {
    sets.value = await fetchAllSets()
})


</script>

<template>
    <PageHeader />
    <h1>Sets</h1>
    <div class="set-holder">
        
        <div v-for="card_set in sets"
            :key="card_set.id"
            class="set-item" 
            @click="router.push(`/sets/${card_set.id}`)">
            <img :src="`${API_URL}/set_logo/${card_set.id}.png`" style="max-width: 100px; max-height: 100px;"/>
            <!-- <p>{{card_set.name}}</p> -->
            <p>{{card_set.release_date}}</p>
        </div>
    </div>
</template>
