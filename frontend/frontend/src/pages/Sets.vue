<script setup lang="ts">
import PageHeader from '../components/PageHeader.vue';
import { onMounted, ref, type Ref } from 'vue';
import type { SetCard } from '../utilities/interfaces';
import { fetchAllSets } from '../utilities/aplFetch';
import { router } from '../main';

onMounted(async() => {
    sets.value = await fetchAllSets()
})
const sets: Ref<SetCard[]> = ref<SetCard[]>([])

function redirectToSetInfo(id: string){
    console.log(id)
    router.push(`/sets/${id}`)
}

</script>

<template>
    <PageHeader />
    <h1>SETOVI</h1>
    <div class="set-holder">
        <div v-for="card_set in sets" :key="card_set.id" class="set-item" @click="redirectToSetInfo(card_set.id)">
            <p>{{card_set.name}}</p>
            <p>{{card_set.release_date}}</p>
        </div>
    </div>
</template>

<style>
.set-holder{
    display: grid;
    grid-template-columns: repeat(10,auto);
    gap: 5px
}

.set-item{
    background-color: darkblue;
    align-content: center;
}

.set-item > p{
    text-align: center;
}

</style>