<script setup lang="ts">
import { onMounted, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import { userName } from '../utilities/constants';
import type { Card } from '../utilities/interfaces';
import CardContainer from '../components/CardContainer.vue';
import api from '../api';
import { accessToken } from '../utilities/userAuthentification';
import placeholder_image from '../assets/placeholder.png'

const collection = ref<Card[]>([])
const wishlist = ref<Card[]>([])
const picture = ref<string>()

const fetchCollection = async() => {

    try{
        const res = await api.get('/collection', {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        collection.value = res.data
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
        picture.value = res.data.picture
        console.log(res.data)
    }
    catch(err){
        console.error(err)
    }
    fetchCollection()
})
</script>

<template>
        <PageHeader/>
        <img v-if="picture" :src="picture || placeholder_image" style="height: 100px; width: 100px; border-radius: 50px;"/>
        <h1> {{ userName }} </h1>
        <h2>Collection</h2>
        <div>
            <CardContainer
                v-if="collection.length!==0"
                :cards="collection"
                :display-info="false"/>
            <div v-else>
                <p>Your collection is empty</p>
                <router-link to="/">Search for more cards</router-link>
            </div>
        </div>
        <h2>Wishlist</h2>
        <div>
            <CardContainer
                v-if="wishlist.length !== 0"
                :cards="wishlist"
                :display-info="false"/>
            <p v-else>You have no items on your wishlist</p>
        </div>

</template>