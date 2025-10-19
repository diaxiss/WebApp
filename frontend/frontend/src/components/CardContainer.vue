<script setup lang="ts">
import '../styles/CardContainer.css'

import { imageFallback } from '../utilities/misc';
import type { Card } from '../utilities/interfaces';
import { accessToken, API_URL, collection, wishlist } from '../utilities/constants';
import FullscreenImage from './FullscreenImage.vue';
import { useWishlist } from '../composables/useWishlist';
import { useCollection } from '../composables/useCollection';
import { useFullscreenImage } from '../composables/useFullscreenImage';

const { openImage } = useFullscreenImage()

const props = defineProps<{
  cards: Card[]
  displayInfo: boolean
  extraOptions: boolean
}>()


const {add: wishlistAdd, remove: wishlistRemove} = useWishlist()
const {add: collectionAdd, remove: collectionRemove} = useCollection()

</script>

<template>

  <FullscreenImage/>

  <div class="query-container">

    <div class="query-item-container" v-for="result in props.cards" :key="result.card_id">

      <img class='card-image' loading="lazy" :src="`${API_URL}/images/${result.card_id}.png`"
        :alt="`${result.name} - ${result.card_id}`" 
        @click="openImage(result.card_id)"
        @error="imageFallback"/>

      <div v-if="displayInfo">
        <p @click="$router.push(`/sets/${result.card_set_id}`)">{{ result.card_set }}</p>
        <p>{{ result.release_date }}</p>
      </div>

      <!-- Extra options for wishlist/collections -->
      <div v-if="extraOptions && accessToken" class="extra-options">
        <div class="wishlist-buttons"
          v-if="!collection.find(card => card.card_id === result.card_id)">
          <button
            v-if="!wishlist.find(card => card.card_id === result.card_id)"
            @click="wishlistAdd(result)">
            <span >♡</span>
          </button>

          <button
            v-else
            @click="wishlistRemove(result)">
            <span>❤️</span>
          </button>
        </div>

        <span>{{ result.count ||
        collection[collection.findIndex(card =>{
          return card.card_id === result.card_id
        })]?.count }}</span>

        <div class="collection-buttons">
          <button 
            @click="collectionAdd(result)">
            <span>+</span>
          </button>

          <button 
            v-if="collection.find(card => card.card_id === result.card_id)"
            @click="collectionRemove(result)">
            <span>-</span>
          </button>
        </div>

      </div>
    </div>
  </div>


</template>