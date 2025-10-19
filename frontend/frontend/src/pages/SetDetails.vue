<script setup lang="ts">

import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import PageHeader from '../components/PageHeader.vue';
import CardContainer from '../components/CardContainer.vue';

import { useCardSearch } from '../composables/useCardSearch';
import { useSets } from '../composables/useSets';
import { API_URL } from '../utilities/constants';

const {fetchSet} = useSets()
const {loadedCards} = useCardSearch()

const route = useRoute()
const set_id: string = route.params.id as string

const imageExists = ref(true)

onMounted(() => {
    fetchSet(set_id)
})


</script>

<template>
    <PageHeader/>
    <img v-if="imageExists" 
        :src="`${API_URL}/set_logo/${set_id}.png`"
        style="max-width: 400px; max-height: 200px;"
        @error="imageExists = false"
    />
    <h1 v-else>{{ loadedCards[0]?.card_set }}</h1>
    <CardContainer
        :cards="loadedCards"
        :display-info="false"
        :extra-options="true"
    />
</template>