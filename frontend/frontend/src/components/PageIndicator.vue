<script setup lang="ts">
import { computed, ref } from 'vue';
import '../styles/PageIndicator.css'
import { currentPage, numOfPages } from '../utilities/constants';

const emits = defineEmits<{
    (e: 'load', value: number): void
}>()

const jumpPage = ref<number>(1)

const pagesToShow = computed(() => {

    const pages = new Array<number | string>();

    pages.push(1)
    if (currentPage.value > 4){
        pages.push('...')
    }

    const start = Math.max(2, currentPage.value-2);
    const end = Math.min(numOfPages.value - 1, currentPage.value + 2)

    for(let i = start; i<= end; i++){
        pages.push(i)
    }
    if (currentPage.value < numOfPages.value-3){
        pages.push('...')
    }

    if (numOfPages.value > 1){
        pages.push(numOfPages.value)
    }
    return pages
})

const handlePageJump = () => {
    if (jumpPage.value > numOfPages.value || jumpPage.value < 1) return
    console.log(jumpPage.value)
    emits('load', jumpPage.value)
}

</script>

<template>
    <div>
        <div class="page-indicator-container">

            <!-- First page -->
            <button :disabled="currentPage === 1" @click="$emit('load', 1)">&lt;&lt;</button>
            <!-- Previous page -->
            <button :disabled="currentPage === 1" @click="$emit('load', currentPage-1)">&lt;</button>
            

            <div v-for="page in pagesToShow" 
                :class="['page-indicator', page === currentPage ? 'disabled' : 'enabled']"
                @click="(page !== currentPage && page !== '...') ? $emit('load', page as number): null">

                <a
                    v-if="page !== '...'" 
                    :key = page
                > 
                {{ page }}
                </a>

                <span v-else>...</span>

            </div>

            <!-- Next page -->
            <button :disabled="currentPage === numOfPages" @click="$emit('load', currentPage+1)">&gt;</button>
            <!-- Last page -->
            <button :disabled="currentPage === numOfPages" @click="$emit('load', numOfPages)">&gt;&gt;</button>
            
        </div>
        <form @submit.prevent="handlePageJump">
            <label for="page-select">Jump to: </label>
            <input id="page-select" type="number" v-model.number="jumpPage"></input>
            <button type="submit">Apply</button>
        </form>
    </div>

</template>