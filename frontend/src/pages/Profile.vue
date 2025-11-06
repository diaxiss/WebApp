<script setup lang="ts">
import { onMounted, ref } from 'vue';

import PageHeader from '../components/PageHeader.vue';
import CardContainer from '../components/CardContainer.vue';

import type { Card } from '../utilities/interfaces';

import { loading } from '../utilities/constants';
import { userName } from '../utilities/constants';

import placeholder_image from '../assets/placeholder.png'
import { useRoute } from 'vue-router';
import { fetchUser } from '../utilities/aplFetch';
import { fetchCollectionSummary } from '../utilities/collection';
import { fetchWishlistSummary } from '../utilities/wishlist';

const collection = ref<Card[]>([])
const wishlist = ref<Card[]>([])
const picture = ref<string | null>()
const profile_user_name = ref<string | null> (userName.value)

const route = useRoute()
const user_id: string = route.params.id as string



onMounted(async() => {


    loading.value = true

    fetchUser(user_id).then((res) => {
        picture.value = res?.picture
        profile_user_name.value = res?.profile_user_name
    })

    collection.value = await fetchCollectionSummary(user_id)
    wishlist.value = await fetchWishlistSummary(user_id)
    loading.value = false
})
</script>

<template>
        <PageHeader/>
        <img v-if="picture" :src="picture || placeholder_image" style="height: 100px; width: 100px; border-radius: 50px;"/>
        <h1> {{ profile_user_name }} </h1>
        <h2>Collection</h2>
        <div>
            <div v-if="collection.length!==0">
                <CardContainer   
                    :cards="collection"
                    :display-info="false"
                    :extra-options="false"/>
                <router-link :to="`/collection/${user_id || ''}`">
                    <button>View whole collection</button>
                </router-link>
            </div>
            <div v-else>
                <p>{{user_id ? 'This' : 'Your'}} collection is empty</p>
                <router-link v-if="!user_id" to="/">Search for more cards</router-link>
            </div>
        </div>
        <h2>Wishlist</h2>
        <div>
            <div v-if="wishlist.length!==0">
                <CardContainer
                    :cards="wishlist"
                    :display-info="false"
                    :extra-options="false"/>
                <router-link :to="`/wishlist/${user_id || ''}`">
                    <button>View whole wishlist</button>
                </router-link>
            </div>
            <p v-else>{{ user_id ? 'There are' : 'You have'}} no items on {{ user_id ? 'this': 'your'}} wishlist</p>
        </div>

</template>