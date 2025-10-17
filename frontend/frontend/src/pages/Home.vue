<style src="../styles/Home.css"></style>
<script setup lang='ts'>

import { onMounted } from 'vue';

import SearchForm from '../components/SearchForm.vue';
import PageHeader from '../components/PageHeader.vue';
import PageIndicator from '../components/PageIndicator.vue';
import CardContainer from '../components/CardContainer.vue';

import { useCardSearch } from '../composables/useCardSearch';

const { loadedCards, fetchAll } = useCardSearch()

onMounted(async () => {
    fetchAll()
})

</script>

<template>

    <PageHeader />

    <SearchForm/>
    <button @click="fetchAll">All cards</button>

    <CardContainer
        :cards="loadedCards"
        :display-info="false"
        :extra-options="true"/>

    <PageIndicator/>

</template>