<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import type { Card } from '../utilities/interfaces';
import { fetchImage } from '../utilities/aplFetch';
import '../styles/CardContainer.css'

defineProps<{
  cards: Card[]
  displayInfo: boolean
}>()

const fullscreenImage = ref<string | null>(null);
const imageWrapper = ref<HTMLElement | null>(null)

function openImage(image: string){
    fullscreenImage.value = image
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
</script>

<template>
    <div class="query-container">

            <div class="query-item-container" v-for="result in cards" :key="result.card_id">
                
                <img 
                    class='card-image'
                    loading="lazy"
                    :src="fetchImage(result.image)"
                    @click="openImage(fetchImage(result.image))">
                <div v-if="displayInfo">
                    <p @click="$router.push(`/sets/${result.card_set_id}`)">{{ result.card_set }}</p>
                    <p>{{ result.release_date }}</p>
                </div>
            </div>

        </div>

        <!-- Fullscreen overlay -->
        <div
            v-if="fullscreenImage"
            class="image-overlay"
            @click.self="closeImage">
            <div
                @mouseenter="handleMouseEnter"
                @mousemove="handleMouseMove"
                @mouseleave="resetTransform"
                class="image-wrapper">
                <img 
                    :src="fullscreenImage"
                    ref="imageWrapper"
/>
            </div>
        </div>
</template>