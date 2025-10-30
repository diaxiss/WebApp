<script setup lang="ts">

import { onMounted } from 'vue';

import CardContainer from '../components/CardContainer.vue';
import PageHeader from '../components/PageHeader.vue';

import { useCollection } from '../composables/useCollection';
import { loading } from '../utilities/constants';

//Composables
const {collection, fetch: fetchCollection } = useCollection()

onMounted(async() => {
    loading.value = true
    await fetchCollection()
    loading.value = false
})

</script>

<template>

    <PageHeader/>
    <h1>Collection</h1>
    <CardContainer
        v-if="collection.length!==0"
        :cards="collection"
        :display-info="false"
        :extra-options="true"/>
    <div v-else>
        <p>Your collection is empty</p>
        <router-link to="/">Search for more cards</router-link>
    </div>
</template>