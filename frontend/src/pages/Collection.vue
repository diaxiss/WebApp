<script setup lang="ts">

import { onMounted } from 'vue';

import CardContainer from '../components/CardContainer.vue';
import PageHeader from '../components/PageHeader.vue';

import { useCollection } from '../composables/useCollection';
import { loading } from '../utilities/constants';
import { useRoute } from 'vue-router';

//Composables
const {collection, fetch: fetchCollection } = useCollection()

const route = useRoute()
const user_id: string = route.params.id as string

onMounted(async() => {
    loading.value = true
    await fetchCollection(user_id)
    loading.value = false
})

</script>

<template>

    <PageHeader/>
    <h1>Collection</h1>
    <CardContainer
        v-if="collection.length!==0"
        :cards="collection"
        :display-info="false"
        :extra-options="user_id ? false : true"/>
    <div v-else>
        <p>{{ user_id ? 'This' : 'Your'}} collection is empty</p>
    </div>
</template>