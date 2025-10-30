<script setup lang="ts">
import '../styles/PageIndicator.css'
import { currentPage, numOfPages } from '../utilities/constants';

import { usePagination } from '../composables/usePagination';
import { useCardSearch } from '../composables/useCardSearch';


const {pagesToShow, handlePageJump, jumpPage} = usePagination()
const {loadMore} = useCardSearch()

</script>

<template>
    <div>
        <div class="page-indicator-container">

            <!-- First page -->
            <button :disabled="currentPage === 1" @click="loadMore(1)">&lt;&lt;</button>
            <!-- Previous page -->
            <button :disabled="currentPage === 1" @click="loadMore(currentPage-1)">&lt;</button>
            

            <div v-for="page in pagesToShow" 
                :class="['page-indicator', page === currentPage ? 'disabled' : 'enabled']"
                @click="(page !== currentPage && page !== '...') ? loadMore(page as number): null">

                <a
                    v-if="page !== '...'" 
                    :key = page
                > 
                {{ page }}
                </a>

                <span v-else>...</span>

            </div>

            <!-- Next page -->
            <button :disabled="currentPage === numOfPages" @click="loadMore(currentPage+1)">&gt;</button>
            <!-- Last page -->
            <button :disabled="currentPage === numOfPages" @click="loadMore(numOfPages)">&gt;&gt;</button>
            
        </div>
        <form @submit.prevent="handlePageJump">
            <label for="page-select">Jump to: </label>
            <input id="page-select" type="number" v-model.number="jumpPage"></input>
            <button type="submit">Apply</button>
        </form>
    </div>

</template>