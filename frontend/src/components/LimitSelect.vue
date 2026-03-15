<script setup lang="ts">
import { usePayloadStore } from '../stores/payloadStore';


const emits = defineEmits(['change'])

const store = usePayloadStore()

</script>

<template>
    <div>
        <label for="limit">Limit per page:</label>
        <select id="limit" v-model.number="store.payload.limit" 
            @change="$emit('change', store.payload.limit)">
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
        </select>
    </div>
</template>