<script setup lang="ts">
import { onMounted, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import type { Card } from '../utilities/interfaces';
import CardContainer from '../components/CardContainer.vue';
import { addToWishlist, fetchWishlist, removeFromWishlist } from '../utilities/wishlist';
import { removeFromCollection, addToCollection } from '../utilities/collection';
import { collection, wishlist } from '../utilities/constants';

const numOfWishlist = ref<number>(0)


async function handleAddToCollection(card: Card){

    const index = collection.value.findIndex(testCard => {
            return testCard.card_id === card.card_id
        })
    if (index !== -1){
        if (collection.value[index]?.count){
            collection.value[index].count += 1
        }
    } else{
        collection.value.push({...card, count: 1})
    }

    let res = await addToCollection(card)

    if (res?.msg == 'Success') {
        await handleRemoveFromWishlist(card)
    }
    else if (collection.value[index]?.count){
        collection.value[index].count -= 1
    }
}

async function handleRemoveFromCollection(card: Card){

    const res = await removeFromCollection(card)

    if (res?.msg == 'Success') return
}

async function handleRemoveFromWishlist(card: Card){

    const index = wishlist.value.findIndex(testCard => {
            return testCard.card_id === card.card_id
        })
    const card_copy = wishlist.value[index] as Card

    wishlist.value.splice(index,1)

    const res = await removeFromWishlist(card)
    if (res?.msg == 'Success') return

    else wishlist.value.splice(index, 0, card_copy)
}

async function handleAddToWishlist(card: Card){
  const res = await addToWishlist(card)
  if (res?.msg == 'Success') return
}

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
        :extra-options="true"
        @collection-add="handleAddToCollection"
        @collection-remove="handleRemoveFromCollection"
        @wishlist-add="handleAddToWishlist"
        @wishlist-remove="handleRemoveFromWishlist"/>
    <p v-else>You have no items on your wishlist</p>
</template>