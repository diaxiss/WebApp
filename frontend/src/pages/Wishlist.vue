<script setup lang="ts">
import { onMounted } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import CardContainer from '../components/CardContainer.vue';

import { useWishlist } from '../composables/useWishlist';
import { loading } from '../utilities/constants';
import { useRoute } from 'vue-router';

const { wishlist, fetch: fetchWishlist } = useWishlist()

const route = useRoute()
const user_id: string = route.params.id as string

onMounted(async() => {
    loading.value = true
    await fetchWishlist(user_id)
    loading.value = false
})
</script>

<template>
    <PageHeader/>
    <h1>Wishlist</h1>
    <CardContainer
        v-if="wishlist.length!==0"
        :cards="wishlist"
        :display-info="false"
        :extra-options="user_id ? false : true"/>
    <p v-else>{{ user_id ? 'There are' : 'You have'}} no items on your wishlist</p>
    <router-link v-if="!user_id" to="/">Search for more cards</router-link>
</template>