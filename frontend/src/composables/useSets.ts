import api from "../api"
import { accessToken } from "../utilities/constants"
import { useCardSearch } from "./useCardSearch"

const { loadedCards } = useCardSearch()

export function useSets(){
    
    const fetchSet = async(set_id: string) => {
        const res = await api.get(`/sets/${set_id}`, {
            headers: {
                Authorization: `Bearer ${accessToken.value}`
            }
        })
        loadedCards.value = res.data.cards
        console.log(loadedCards.value)
    }
    return {fetchSet}
}