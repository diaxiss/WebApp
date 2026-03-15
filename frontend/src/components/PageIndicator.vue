<script setup lang="ts">
import '../styles/PageIndicator.css'

import { usePagination } from '../composables/usePagination';
import { computed } from 'vue';
import { usePayloadStore } from '../stores/payloadStore';

const store = usePayloadStore()

const emits = defineEmits(['loadMore'])

const props = defineProps<{
    data: Array<any>
    total_data_size: number
}>()


const {currentPage, 
        jumpPage, 
        numOfPages, 
        pagesToShow
} = usePagination(
        computed(() => props.total_data_size),
        computed(() => store.payload.limit)
)

const handleSelect = (page: number) => {
    currentPage.value = page
    store.payload.offset = store.payload.limit * (page-1)
    emits('loadMore', currentPage.value)
}

const handlePageJump = () => {
    currentPage.value = Math.min(jumpPage.value, numOfPages.value)
    emits('loadMore', currentPage.value)
}

</script>

<template>
    <div>
        <div class="page-indicator-container">

            <!-- First page -->
            <button :disabled="currentPage === 1" @click="handleSelect(1)">&lt;&lt;</button>
            <!-- Previous page -->
            <button :disabled="currentPage === 1" @click="handleSelect(currentPage-1)">&lt;</button>
            

            <div v-for="page in pagesToShow" 
                :class="['page-indicator', 
                        page === currentPage ? 'disabled' : 'enabled']"
                @click="(page !== currentPage && page !== '...') ? handleSelect(page as number): null">

                <a
                    v-if="page !== '...'" 
                    :key = page
                > 
                {{ page }}
                </a>

                <span v-else>...</span>

            </div>

            <!-- Next page -->
            <button :disabled="currentPage === numOfPages" @click="handleSelect(currentPage+1)">&gt;</button>
            <!-- Last page -->
            <button :disabled="currentPage === numOfPages" @click="handleSelect(numOfPages)">&gt;&gt;</button>
            
        </div>
        <form @submit.prevent="handlePageJump">
            <label for="page-select">Jump to: </label>
            <input id="page-select" type="number" v-model.number="jumpPage"></input>
            <button type="submit">Apply</button>
        </form>
    </div>

</template>