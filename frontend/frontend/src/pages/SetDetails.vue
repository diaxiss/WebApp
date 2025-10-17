<script setup lang="ts">

import { onMounted } from 'vue';
import { useRoute } from 'vue-router';

import PageHeader from '../components/PageHeader.vue';
import CardContainer from '../components/CardContainer.vue';

import { useCardSearch } from '../composables/useCardSearch';
import { useSets } from '../composables/useSets';

const {fetchSet} = useSets()
const {loadedCards} = useCardSearch()

const route = useRoute()
const set_id: string = route.params.id as string


onMounted(() => {
    fetchSet(set_id)
})


</script>

<template>
    <PageHeader/>
    <h1> {{ loadedCards[0]?.card_set }} </h1>
    <CardContainer
        :cards="loadedCards"
        :display-info="false"
        :extra-options="true"
    />
</template>