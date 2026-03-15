import { ref } from "vue";
import type { Card, SearchPayload } from "../utilities/interfaces";
import { fetchAllCards, queryCards } from "../utilities/aplFetch";

const loadedCards = ref<Card[]>([])
const isQueried = ref(false);

export function useCardSearch() {



    const truncatePayload = (payload: SearchPayload) => {
        (Object.keys(payload) as Array<keyof SearchPayload>).forEach(key =>{
            if (payload[key] === '' || payload[key] === null){
                delete payload[key];
            }
        })
        if (Object.keys(payload).length < 2 && isQueried.value){
            console.log('Not enough form data')
            fetchCards({payload: payload})
            return false
        }
        return true

    }

    async function fetchCards({ payload = {} as SearchPayload , query = false, page = 1} = {}){
        payload.offset = payload.limit * (page-1);
        isQueried.value = query
        if (!truncatePayload(payload)) return [[], 0]

        const res = query ? await queryCards(payload) : await fetchAllCards(payload)
        if (res){
            return [res.cards as Card[], res.numOfCards as number]
        }
        return [[], 0]
    }

    async function fetchAll(payload: SearchPayload, page: number = 1) {
        return await fetchCards({payload: payload, query: false, page: page}) as [Card[], number]
    }

    async function fetchQuery(payload: SearchPayload, page: number = 1) {
        return await fetchCards({ payload: payload, query: true, page: page}) as [Card[], number]
    }

    return {loadedCards, isQueried, fetchAll, fetchQuery}

}