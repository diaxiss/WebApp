<script setup lang="ts">

import '../styles/FullscreenImage.css'

import { useFullscreenImage } from '../composables/useFullscreenImage';

const { closeImage, 
    fullscreenImage, imageWrapper, 
    handleMouseEnter, handleMouseMove, 
    resetTransform} = useFullscreenImage()

</script>

<template>
    <!-- Fullscreen overlay -->
  <div v-if="fullscreenImage"
    class="image-overlay" 
    @click.self="closeImage">

    <div
      class="image-wrapper"
      @mouseenter="handleMouseEnter"
      @mousemove="handleMouseMove"
      @mouseleave="resetTransform">

      <img :alt="fullscreenImage" :src="fullscreenImage" ref="imageWrapper" />
    
    </div>
  </div>
</template>