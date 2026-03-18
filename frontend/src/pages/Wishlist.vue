<script setup lang="ts">
import { onMounted, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import CardContainer from '../components/CardContainer.vue';

import { useWishlist } from '../composables/useWishlist';
import { loading } from '../utilities/constants';
import { useRoute } from 'vue-router';
import LimitSelect from '../components/LimitSelect.vue';
import PageIndicator from '../components/PageIndicator.vue';
import type { Card } from '../utilities/interfaces';
import { usePayloadStore } from '../stores/payloadStore';

const store = usePayloadStore()

const route = useRoute()
const user_id: string = route.params.id as string

const wishlist = ref<Card[]>([]);
const wishlistLength = ref<number>(0) 

const { fetch: fetchWishlist } = useWishlist(wishlist)

const handleChange = async() => {
    [wishlist.value, wishlistLength.value] = await fetchWishlist(store.payload.limit, store.payload.offset, user_id)
}

const handleLoadMore = async(page: number) => {
    [wishlist.value, wishlistLength.value] = await fetchWishlist(store.payload.limit, store.payload.limit*(page-1))
}

onMounted(async() => {
    loading.value = true;
    [store.payload.limit, store.payload.offset] = [25,0];
    [wishlist.value, wishlistLength.value] = await fetchWishlist(store.payload.limit, store.payload.offset, user_id)
    loading.value = false
})

</script>

<template>
    <PageHeader/>
    <h1>Wishlist</h1>
    <LimitSelect @change="handleChange"/>

    <CardContainer
        v-if="wishlist.length!==0"
        :cards="wishlist"
        :displayInfo="true"
        :extraOptions="user_id ? false : true"/>

    <p v-else>{{ user_id ? 'There are' : 'You have'}} no items on your wishlist</p>

    <PageIndicator
        @load-more="handleLoadMore"
        :data="wishlist"
        :total_data_size="wishlistLength"
        :limit="store.payload.limit"
        :offset="store.payload.offset"/>
</template>