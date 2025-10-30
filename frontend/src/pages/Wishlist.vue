<script setup lang="ts">
import { onMounted } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import CardContainer from '../components/CardContainer.vue';

import { useWishlist } from '../composables/useWishlist';

const { wishlist, fetch: fetchWishlist } = useWishlist()

onMounted(async() => {
    fetchWishlist()
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