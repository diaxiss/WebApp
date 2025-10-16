<script setup lang="ts">
import { onMounted, ref } from 'vue';
import CardContainer from '../components/CardContainer.vue';
import PageHeader from '../components/PageHeader.vue';
import type { Card } from '../utilities/interfaces';
import { addToCollection, fetchCollection, removeFromCollection } from '../utilities/collection';
import { removeFromWishlist, addToWishlist } from '../utilities/wishlist';
import { collection } from '../utilities/constants';

const numOfCollection = ref<number>(0)


async function handleAddToCollection(card: Card){

    const index = collection.value.findIndex(testCard => {
            return testCard.card_id === card.card_id
        })
    if (index !== -1){
        if (collection.value[index]?.count){
            collection.value[index].count += 1
        }
    }

    const res = await addToCollection(card)
    if (res?.msg == 'Success') return

    else if (collection.value[index]?.count){
        collection.value[index].count -= 1
    }
}

async function handleRemoveFromCollection(card: Card){

    const index = collection.value.findIndex(testCard => {
            return testCard.card_id === card.card_id
        })

    const card_copy = {...collection.value[index]} as Card

    if (index !== -1 && collection.value[index]?.count){
        collection.value[index].count -= 1

        if (collection.value[index].count < 1){
            collection.value.splice(index, 1)
        }
    }

    const res = await removeFromCollection(card)
    if (res?.msg == 'Success') return

    if (!collection.value[index]?.count){
        collection.value.splice(index, 0, card_copy)
    }
    else collection.value[index].count += 1
}

async function handleRemoveFromWishlist(card: Card){
    const res = await removeFromWishlist(card)

    if (res?.msg == 'Success') return
}

async function handleAddToWishlist(card: Card){
 const res = await addToWishlist(card)

    if (res?.msg == 'Success') return
}

onMounted(async() => {
    const response = await fetchCollection()
    collection.value = response.collection
    numOfCollection.value = response.numOfCollection
    console.log(collection.value, numOfCollection.value)
})

</script>

<template>

    <PageHeader/>
    <h1>Collection</h1>
    <CardContainer
        v-if="collection.length!==0"
        :cards="collection"
        :display-info="false"
        :extra-options="true"
        @collection-add="handleAddToCollection"
        @collection-remove="handleRemoveFromCollection"
        @wishlist-add="handleAddToWishlist"
        @wishlist-remove="handleRemoveFromWishlist"
    />
    <div v-else>
        <p>Your collection is empty</p>
        <router-link to="/">Search for more cards</router-link>
    </div>
</template>