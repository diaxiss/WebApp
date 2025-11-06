import { ref } from "vue";
import type { Card, SearchPayload } from "../utilities/interfaces";
import { currentPage, numOfCards, numOfPages, payload } from "../utilities/constants";
import { fetchAllCards, queryCards } from "../utilities/aplFetch";

const loadedCards = ref<Card[]>([])
const isQueried = ref(false);

export function useCardSearch() {



    const truncatePayload = () => {
        (Object.keys(payload) as Array<keyof SearchPayload>).forEach(key =>{
            if (payload[key] === '' || payload[key] === null){
                delete payload[key];
            }
        })

        if (Object.keys(payload).length <= 2 && isQueried.value){
            console.log('Not enough form data')
            fetchCards()
            return false
        }
        return true

    }

    async function fetchCards({ query = false, page = 1} = {}){
        payload.offset = payload.limit * (page-1);
        currentPage.value = page
        isQueried.value = query
        if (!truncatePayload()) return


        const res = query ? await queryCards() : await fetchAllCards()
        if (res){
            loadedCards.value = [...res.cards]
            numOfCards.value = res.numOfCards
            numOfPages.value = Math.ceil(numOfCards.value/payload.limit)
        }
    }

    async function fetchAll() {
        await fetchCards({query: false, page: 1})
    }

    async function fetchQuery() {
        await fetchCards({ query: true, page: 1})
    }

    async function loadMore( page: number ){
        await fetchCards( {query: isQueried.value, page })
    }

    async function setLimit(){

        payload.offset = 0;
        currentPage.value = 1;
        await fetchCards({ query: isQueried.value, page: 1 })
    }

    return {loadedCards, isQueried, fetchAll, fetchQuery, loadMore, setLimit}

}