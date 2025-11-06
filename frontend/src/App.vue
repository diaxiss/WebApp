<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import { useWishlist } from './composables/useWishlist';
import { useCollection } from './composables/useCollection';
import { onMounted } from 'vue';

const {fetch: fetchWishlist} = useWishlist()
const {fetch: fetchCollection} = useCollection()

const route = useRoute()

onMounted(async() => {
  if (localStorage.getItem('accessToken')){
    fetchWishlist()
    fetchCollection()
  }
})

</script>

<template>
  <RouterView :key="route.fullPath"/>
</template>