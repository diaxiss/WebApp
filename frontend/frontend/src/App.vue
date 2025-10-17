<script setup lang="ts">
import { RouterView } from 'vue-router';
import { useWishlist } from './composables/useWishlist';
import { useCollection } from './composables/useCollection';
import { onMounted } from 'vue';

const {fetch: fetchWishlist} = useWishlist()
const {fetch: fetchCollection} = useCollection()

onMounted(async() => {
  fetchWishlist()
  fetchCollection()
})

</script>

<template>
  <RouterView/>
</template>