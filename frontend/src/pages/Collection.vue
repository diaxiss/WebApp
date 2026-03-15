<script setup lang="ts">

import { onMounted, ref } from 'vue';

import CardContainer from '../components/CardContainer.vue';
import PageHeader from '../components/PageHeader.vue';
import PageIndicator from '../components/PageIndicator.vue';
import LimitSelect from '../components/LimitSelect.vue';

import { useCollection } from '../composables/useCollection';
import { loading } from '../utilities/constants';
import { useRoute } from 'vue-router';
import type { Card } from '../utilities/interfaces';
import { usePayloadStore } from '../stores/payloadStore';

const collection = ref<Card[]>([])
const collectionLength = ref<number>(0)

const { fetch: fetchCollection } = useCollection(collection)

const store = usePayloadStore()

const route = useRoute()
const user_id: string = route.params.id as string

const handleChangeLimit = async() => {
    [collection.value, collectionLength.value] = await fetchCollection(store.payload.limit, store.payload.offset, user_id)
}

const handlePageChange = async(page: number) => {
    [collection.value, collectionLength.value] = await fetchCollection(store.payload.limit, store.payload.limit * (page-1))
}

onMounted(async() => {
    loading.value = true;
    [store.payload.limit, store.payload.offset] = [25,0];
    [collection.value, collectionLength.value] = await fetchCollection(store.payload.limit, store.payload.offset, user_id)
    loading.value = false
    console.log(collection.value)
})

</script>

<template>

    <PageHeader/>
    <h1>Collection</h1>
    <LimitSelect
        @change="handleChangeLimit"
    />
    <CardContainer
        v-if="collection.length!==0"
        :cards="collection"
        :display-info="false"
        :extra-options="user_id ? false : true"/>
    <div v-else>
        <p>{{ user_id ? 'This' : 'Your'}} collection is empty</p>
    </div>
    <PageIndicator
        @load-more="handlePageChange"
        :data="collection"
        :total_data_size="collectionLength"
        :limit="store.payload.limit"
        :offset="store.payload.offset"/>
</template>