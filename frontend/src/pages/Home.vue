<style src="../styles/Home.css"></style>
<script setup lang='ts'>

import { onMounted, ref } from 'vue';

import SearchForm from '../components/SearchForm.vue';
import PageHeader from '../components/PageHeader.vue';
import PageIndicator from '../components/PageIndicator.vue';
import CardContainer from '../components/CardContainer.vue';

import { useCardSearch } from '../composables/useCardSearch';
import { loading } from '../utilities/constants';
import type { Card } from '../utilities/interfaces';
import { usePayloadStore } from '../stores/payloadStore';

const { fetchAll } = useCardSearch()

const store = usePayloadStore()

const cards = ref<Card[]>([]);
const cardsLength = ref<number>(0);

const { fetchQuery } = useCardSearch()

const handleCardSubmit = (new_cards: [Card[], number]) => {
    [cards.value, cardsLength.value] = new_cards
}

const handlePageChange = async(page: number) => {
    [cards.value, cardsLength.value] = await fetchQuery(store.payload, page)
}

onMounted(async () => {
    loading.value = true;
    [store.payload.limit, store.payload.offset] = [10, 0];
    [cards.value, cardsLength.value] = await fetchAll({...store.payload})
    loading.value = false
})
</script>

<template>

    <PageHeader />

    <SearchForm @submit="handleCardSubmit"/>
    <button 
        @click="{fetchAll(store.payload); store.clearPayload()}">
            All cards
    </button>

    <CardContainer
        :cards="cards"
        :display-info="true"
        :extra-options="true"/>

    <PageIndicator
        @load-more="handlePageChange"
        :data="cards"
        :total_data_size="cardsLength"
        :limit="store.payload.limit"
        :offset="store.payload.offset"/>

</template>