<script setup lang="ts">
import { useRoute } from 'vue-router';
import api from '../api';
import { onMounted, ref } from 'vue';
import type { Card } from '../utilities/interfaces';
import PageHeader from '../components/PageHeader.vue';
import CardContainer from '../components/CardContainer.vue';



const route = useRoute()
const set_id: string = route.params.id as string
const cards = ref<Card[]>([])

onMounted(() => {
    const fetchSet = async() => {
        const res = await api.get(`/sets/${set_id}`)
        cards.value = res.data.cards
        console.log(cards.value)

    }
    fetchSet()
})


</script>

<template>
    <PageHeader/>
    <h1> {{ cards[0]?.card_set }} </h1>
    <CardContainer
        :cards="cards"
        :display-info="false"
    />
</template>