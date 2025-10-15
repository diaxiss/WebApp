<script setup lang="ts">
import { onMounted, ref } from 'vue';
import CardContainer from '../components/CardContainer.vue';
import PageHeader from '../components/PageHeader.vue';
import type { Card } from '../utilities/interfaces';
import { fetchCollection } from '../utilities/aplFetch';

const collection = ref<Card[]>([])
const numOfCollection = ref<number>(0)



onMounted(async() => {
    const response = await fetchCollection()
    collection.value = response.collection
    numOfCollection.value = response.numOfCollection
    console.log(collection.value)
})

</script>

<template>
    <PageHeader/>
    <h1>Collection</h1>
    <CardContainer
        v-if="collection.length!==0"
        :cards="collection"
        :display-info="false"
        :extra-options="true"
    />
    <div v-else>
        <p>Your collection is empty</p>
        <router-link to="/">Search for more cards</router-link>
    </div>
</template>