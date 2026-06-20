import { ref } from "vue";
import type { Card } from "../utilities/interfaces";
import { fetchAllCards, queryCards } from "../utilities/aplFetch";
import { usePayloadStore } from "../stores/payloadStore";

const loadedCards = ref<Card[]>([])
const isQueried = ref(false);

export function useCardSearch() {

    async function fetchCards({query = false, page = 1}){
        const store = usePayloadStore();

        store.payload.offset = store.payload.limit * (page-1) | 0;

        const res = query ? await queryCards(store.payload) : await fetchAllCards(store.payload)
        if (res){
            return [res.cards as Card[], res.numOfCards as number]
        }
        return [[], 0]
    }

    async function fetchAll(page: number = 1) {
        return await fetchCards({query: false, page: page}) as [Card[], number]
    }

    async function fetchQuery(page: number = 1) {
        return await fetchCards({query: true, page: page}) as [Card[], number]
    }

    return {loadedCards, isQueried, fetchAll, fetchQuery}

}