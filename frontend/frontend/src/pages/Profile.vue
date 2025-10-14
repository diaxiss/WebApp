<script setup lang="ts">
import { onMounted, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import { userName } from '../utilities/constants';
import type { Card } from '../utilities/interfaces';
import CardContainer from '../components/CardContainer.vue';
import api from '../api';
import { accessToken } from '../utilities/userAuthentification';
import placeholder_image from '../assets/placeholder.png'
import { fetchImage } from '../utilities/aplFetch';

const collection = ref<Card[]>([])
const numOfCollection = ref<number>(0)
const wishlist = ref<Card[]>([])
const numOfWishlist = ref<number>(0)
const picture = ref<string | null>()

const fetchCollection = async() => {

    try{
        const res = await api.get('/collection', {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        collection.value = res.data.cards
        numOfCollection.value = res.data.numOfCards
        console.log(res.data)
    }
    catch(err){
        console.error(err)
    }
}

const fetchWishlist = async() => {

    try{
        const res = await api.get('/wishlist', {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        wishlist.value = res.data.cards
        numOfWishlist.value = res.data.numOfCards
        console.log(res.data)
    }
    catch(err){
        console.error(err)
    }
}

onMounted(async() => {
    try{
        const res = await api.get('/user', {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        picture.value = await fetchImage(res.data.picture, 'user_images')
        console.log(res.data)
    }
    catch(err){
        console.error(err)
    }
    fetchCollection()
    fetchWishlist()
})
</script>

<template>
        <PageHeader/>
        <img v-if="picture" :src="picture || placeholder_image" style="height: 100px; width: 100px; border-radius: 50px;"/>
        <h1> {{ userName }} </h1>
        <h2>Collection</h2>
        <div>
            <div v-if="collection.length!==0">
                <CardContainer   
                    :cards="collection"
                    :display-info="false"
                    :extra-options="false"/>
                <button v-if="numOfCollection >= 10">View whole collection</button>
            </div>
            <div v-else>
                <p>Your collection is empty</p>
                <router-link to="/">Search for more cards</router-link>
            </div>
        </div>
        <h2>Wishlist</h2>
        <div>
            <div v-if="wishlist.length!==0">
                <CardContainer
                    :cards="wishlist"
                    :display-info="false"
                    :extra-options="false"/>
                <button v-if="numOfWishlist >= 10">View whole wishlist</button>
            </div>
            <p v-else>You have no items on your wishlist</p>
        </div>

</template>