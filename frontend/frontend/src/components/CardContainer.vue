<script setup lang="ts">
import '../styles/CardContainer.css'

import { onMounted, onUnmounted, ref } from 'vue';

import placeholder_image from '../assets/placeholder.png'
import { imageFallback } from '../utilities/misc';
import type { Card } from '../utilities/interfaces';
import { collection, wishlist } from '../utilities/constants';

const props = defineProps<{
  cards: Card[]
  displayInfo: boolean
  extraOptions: boolean
}>()

const emits = defineEmits<{
  (e: 'wishlistAdd', card: Card): void;
  (e: 'wishlistRemove', card: Card): void;
  (e: 'collectionAdd', card: Card): void;
  (e: 'collectionRemove', card: Card): void;
}>();

const fullscreenImage = ref<string | null>(null);
const imageWrapper = ref<HTMLElement | null>(null)


//----------------------
// Fullscreen card
//----------------------
async function openImage(image: string | null){
    fullscreenImage.value = image ? `http://localhost:8000/images/${image}` : placeholder_image
}

function closeImage(){
    fullscreenImage.value = null
}

function handleMouseEnter() {
  if (!imageWrapper.value) return

  void imageWrapper.value.offsetWidth;

  // Temporary small transition on hover start
  imageWrapper.value.style.transition = 'transform 0.2s cubic-bezier(0.22, 1, 0.36, 1)'
  imageWrapper.value.style.transform = 'perspective(800px) scale(1.05)'
}

function handleMouseMove(e: MouseEvent){
    if(!imageWrapper.value) return

    const rect = imageWrapper.value.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    const centerX = rect.width / 2
    const centerY = rect.height / 2

    const rotateX = ((y- centerY) / centerY) * -10
    const rotateY = ((x- centerX) / centerX) * 10

    imageWrapper.value.style.transition = `transform 0.1s ease-out`
    imageWrapper.value.style.transform = `
        perspective(800px)
        rotateX(${rotateX}deg)
        rotateY(${rotateY}deg)
        scale(1.05)
    `
}

function resetTransform(){

    if(!imageWrapper.value) return
    imageWrapper.value.style.transition = `transform 0.2s ease-in`;
    imageWrapper.value.style.transform = `
        perspective(800px)
        rotateX(0deg)
        rotateY(0deg)
        scale(1)
    `
}

// Close on Esc key
onMounted(() => {
  window.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeImage()
  })  
})
onUnmounted(() => {
  window.removeEventListener('keydown', e => {
    if (e.key === 'Escape') closeImage()
  })
})

</script>

<template>
  <div class="query-container">

    <div class="query-item-container" v-for="result in props.cards" :key="result.card_id">

      <img class='card-image' loading="lazy" :src="`http://localhost:8000/images/${result.image}`"
        :alt="`${result.name} - ${result.card_id}`" 
        @click="openImage(result.image)"
        @error="imageFallback"/>

      <div v-if="displayInfo">
        <p @click="$router.push(`/sets/${result.card_set_id}`)">{{ result.card_set }}</p>
        <p>{{ result.release_date }}</p>
      </div>

      <!-- Extra options for wishlist/collections -->
      <div v-if="extraOptions" class="extra-options">
        <div class="wishlist-buttons"
          v-if="!collection.find(card => card.card_id === result.card_id)">
          <button
            v-if="!wishlist.find(card => card.card_id === result.card_id)"
            @click="$emit('wishlistAdd', result)">
            <span >♡</span>
          </button>

          <button
            v-else
            @click="$emit('wishlistRemove', result)">
            <span>❤️</span>
          </button>
        </div>

        <span>{{ result.count ||
        collection[collection.findIndex(card =>{
          return card.card_id === result.card_id
        })]?.count }}</span>

        <div class="collection-buttons">
          <button 
            @click="$emit('collectionAdd', result)">
            <span>+</span>
          </button>

          <button 
            v-if="collection.find(card => card.card_id === result.card_id)"
            @click="$emit('collectionRemove', result)">
            <span>-</span>
          </button>
        </div>

      </div>

    </div>
  </div>

  <!-- Fullscreen overlay -->
  <div v-if="fullscreenImage" class="image-overlay" @click.self="closeImage">
    <div @mouseenter="handleMouseEnter" @mousemove="handleMouseMove" @mouseleave="resetTransform" class="image-wrapper">
      <img :alt="fullscreenImage" :src="fullscreenImage" ref="imageWrapper" />
    </div>
  </div>
</template>