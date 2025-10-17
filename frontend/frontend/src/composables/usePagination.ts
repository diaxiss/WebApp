import { ref, computed } from "vue";

import { useCardSearch } from "./useCardSearch";

import { currentPage, numOfPages } from "../utilities/constants";

const {loadMore} = useCardSearch()

export function usePagination(){

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
        loadMore(jumpPage.value)
    }

    return { jumpPage, pagesToShow, handlePageJump}
}