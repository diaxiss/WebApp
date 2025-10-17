<script setup lang="ts">
import { RouterView } from 'vue-router';
import { useWishlist } from './composables/useWishlist';
import { useCollection } from './composables/useCollection';
import { onMounted } from 'vue';
import { isLoggedOut } from './utilities/constants';

const {fetch: fetchWishlist} = useWishlist()
const {fetch: fetchCollection} = useCollection()

onMounted(async() => {
  if (!isLoggedOut){
    fetchWishlist()
    fetchCollection()
  }
})

</script>

<template>
  <RouterView/>
</template>