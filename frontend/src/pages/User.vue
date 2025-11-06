<script setup lang="tsx">

import loading_gif from '../assets/loading.gif'
import { onMounted, ref } from 'vue';
import { API_URL, loading } from '../utilities/constants';
import { fetchAllUsers } from '../utilities/aplFetch';
import type { User } from '../utilities/interfaces';
import PageHeader from '../components/PageHeader.vue';
import { useRouter } from 'vue-router';

const users = ref<User[]>([]);
const router = useRouter()

onMounted(async() => {
    loading.value = true
    users.value = await fetchAllUsers()
    console.log(users.value)
    
    loading.value = false
})
</script>

<template>

    <PageHeader/>
    <h1>All users</h1>

    <div v-if="!loading"
        style="display: flex; gap: 10px;">
        <div v-for="user in users"
            @click="router.push(`/profile/${user.picture.split('.')[0]}`)">
            <img :src="`${API_URL}/user_images/${user.picture}`"/>
            <p>{{ user.name }}</p>
        </div>
    </div>

    <div v-else style="width: 100%; display: flex; justify-content: center;">
      <img :src="loading_gif" style="height: 100px; width: 100px"/>
    </div>


</template>