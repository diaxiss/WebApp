<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import type { Card } from '../utilities/interfaces';
import { fetchImage } from '../utilities/aplFetch';
import '../styles/CardContainer.css'
import placeholder_image from '../assets/placeholder.png'
import { handleAddToWishlist } from '../utilities/aplFetch';
import { handleAddToCollection } from '../utilities/aplFetch';
import { handleRemoveFromCollection } from '../utilities/aplFetch';
import { handleRemoveFromWishlist } from '../utilities/aplFetch';

const props = defineProps<{
  cards: Card[]
  displayInfo: boolean
  extraOptions: boolean
}>()

const images = ref<Record<string, string>>({})
const fullscreenImage = ref<string | null>(null);
const imageWrapper = ref<HTMLElement | null>(null)


async function openImage(image: string | null){
    const result_image = await fetchImage(image, 'images')
    console.log(result_image)
    fullscreenImage.value = result_image
}

function closeImage(){
    fullscreenImage.value = null
}

function handleMouseEnter() {
  if (!imageWrapper.value) return

  // Temporary small transition on hover start
  imageWrapper.value.style.transition = 'transform 0.15s ease-out'
  
  // Remove it almost immediately so mousemove is instant
  setTimeout(() => {
    if (imageWrapper.value) imageWrapper.value.style.transition = 'none'
  }, 200) // 50ms is enough to apply a subtle effect
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

watch(
  () => props.cards,
  async (newCards) => {
    const newImages: Record<string, string> = {}
    for (const card of newCards){
      try{
        newImages[card.card_id] = await fetchImage(card.image, 'images')
      }
      catch(err){
        console.error(err)
        newImages[card.card_id] = placeholder_image
      }
    }
    images.value = newImages
  },
  {immediate:true, deep: true}
)

</script>

<template>
  <div class="query-container">

    <div class="query-item-container" v-for="result in cards" :key="result.card_id">

      <img class='card-image' loading="lazy" :src="images[result.card_id] || placeholder_image"
        :alt="`${result.name} - ${result.card_id}`" @click="openImage(result.image)">

      <div v-if="displayInfo">
        <p @click="$router.push(`/sets/${result.card_set_id}`)">{{ result.card_set }}</p>
        <p>{{ result.release_date }}</p>
      </div>

      <!-- Extra options for wishlist/collections -->
      <div v-if="extraOptions" class="extra-options">

        <button @click="handleAddToWishlist(result.card_id)">
          <span >❤️</span>
        </button>

        <button @click="handleRemoveFromWishlist(result.card_id)">
          <span>💔</span>
        </button>

        <button @click="handleAddToCollection(result.card_id, 1)">
          <span>+</span>
        </button>

        <button @click="handleRemoveFromCollection(result.card_id, 1)">
          <span>-</span>
        </button>
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