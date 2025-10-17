import api from "../api"
import { useCardSearch } from "./useCardSearch"

const { loadedCards } = useCardSearch()

export function useSets(){
    
    const fetchSet = async(set_id: string) => {
        const res = await api.get(`/sets/${set_id}`)
        loadedCards.value = res.data.cards
        console.log(loadedCards.value)
    }
    return {fetchSet}
}