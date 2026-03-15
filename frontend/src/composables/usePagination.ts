import { ref, computed, type Ref } from "vue";

export function usePagination(
    total_data_size: Ref<number>,
    limit: Ref<number>,
){

    const currentPage = ref<number>(1)
    const jumpPage = ref<number>(1)

    currentPage.value = 1

    const numOfPages = computed(() => {
        return Math.ceil(total_data_size.value/limit.value)
    })

    const pagesToShow = computed(() => {

        const pages = new Array<number | string>();

        pages.push(1)
        if (currentPage.value > 3){
            pages.push('...')
        }

        const start = Math.max(2, currentPage.value-1);
        const end = Math.min(numOfPages.value - 1, currentPage.value + 1)

        for(let i = start; i<= end; i++){
            pages.push(i)
        }
        if (currentPage.value < numOfPages.value-2){
            pages.push('...')
        }

        if (numOfPages.value > 1){
            pages.push(numOfPages.value)
        }
        return pages
    })

    return { currentPage, jumpPage, numOfPages, pagesToShow }
}