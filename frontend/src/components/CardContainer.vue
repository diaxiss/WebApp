<script setup lang="ts">
import '../styles/CardContainer.css'


import FullscreenImage from './FullscreenImage.vue';

import { imageFallback } from '../utilities/misc';
import type { Card } from '../utilities/interfaces';
import { API_URL, isLoggedOut, loading } from '../utilities/constants';

import { useWishlist } from '../composables/useWishlist';
import { useCollection } from '../composables/useCollection';
import { useFullscreenImage } from '../composables/useFullscreenImage';

import loading_gif from '../assets/loading.gif'
import { computed } from 'vue';

const { openImage } = useFullscreenImage()

const props = defineProps<{
  cards: Card[]
  displayInfo: boolean
  extraOptions: boolean
}>()


const {add: wishlistAdd, remove: wishlistRemove} = useWishlist(computed(() => props.cards))
const {add: collectionAdd, remove: collectionRemove} = useCollection(computed(() => props.cards))


</script>

<template>

  <FullscreenImage/>

  <div class="query-container"
        v-if="!loading">

    <div class="query-item-container" v-for="result in props.cards" :key="result.card_id">

      <div class="image-div">
        <img class='card-image'
          loading="lazy"
          :src="`${API_URL}/images/${result.card_id}.png`"
          :alt="`${result.name} - ${result.card_id}`"
          @click="openImage(result.card_id)"
          @error="imageFallback"/>
          <p class="image-overlay-text">{{result.name}}</p>
      </div>

      <div v-if="displayInfo">
        <p @click="$router.push(`/sets/${result.card_set_id}`)">{{ result.card_set }}</p>
        <p>{{ result.release_date }}</p>
      </div>

      <!-- Extra options for wishlist/collections -->
      <div v-if="extraOptions && !isLoggedOut" class="extra-options">
      
        <div class="wishlist-buttons">
          <button
            v-if="!result.in_wishlist"
            @click="wishlistAdd(result)">
            <span >♡</span>
          </button>

          <button
            v-else
            @click="wishlistRemove(result)">
            <span>❤️</span>
          </button>
        </div>

        <div class="collection-buttons">

          <button 
            v-if="true"
            @click="collectionRemove(result)">
            <span>-</span>
          </button>

          <span>{{ result.count ||
          cards[cards.findIndex(card =>{
            return (card.card_id === result.card_id)
          })]?.count || null }}</span>
          
          <button 
            @click="collectionAdd(result)">
            <span>+</span>
          </button>
          
        </div>

      </div>
    </div>
  </div>

  <div v-else style="width: 100%; display: flex; justify-content: center;">
      <img :src="loading_gif" style="height: 20rem; width: 20rem"/>
  </div>


</template>