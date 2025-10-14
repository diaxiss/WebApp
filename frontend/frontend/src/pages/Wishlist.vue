<script setup lang="ts">
import { onMounted, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import type { Card } from '../utilities/interfaces';
import CardContainer from '../components/CardContainer.vue';
import { fetchWishlist } from '../utilities/aplFetch';

const wishlist = ref<Card[]>([])
const numOfWishlist = ref<number>(0)


onMounted(async() => {
    const response = await fetchWishlist()
    wishlist.value = response.wishlist
    numOfWishlist.value = response.numOfWishlist
})
</script>

<template>
    <PageHeader/>
    <h1>Wishlist</h1>
    <CardContainer
        v-if="wishlist.length!==0"
        :cards="wishlist"
        :display-info="false"
        :extra-options="true"/>
    <p v-else>You have no items on your wishlist</p>
</template>