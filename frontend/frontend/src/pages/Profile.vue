<script setup lang="ts">
import { onMounted, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import { userName } from '../utilities/constants';
import type { Card } from '../utilities/interfaces';
import CardContainer from '../components/CardContainer.vue';
import api from '../api';

const collection = ref<Card[]>([])
const wishlist = ref<Card[]>([])
const picture = ref<string>()

console.log(collection.value.length)

console.log(userName.value)

onMounted(async() => {
    try{
        const res = await api.get('/user')
        picture.value = res.data.picture
        console.log(picture.value)
    }
    catch(err){
        console.error(err)
    }
})
</script>

<template>
        <PageHeader/>
        <img v-if="picture" :src="picture" style="height: 300px;"/>
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