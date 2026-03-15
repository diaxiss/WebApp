import type { Ref } from "vue"
import { addToCollection, fetchCollection, removeFromCollection } from "../utilities/collection"
import type { Card } from "../utilities/interfaces"
import { removeFromWishlist } from "../utilities/wishlist"


export function useCollection(collection: Ref<Card[]>) {
    const add = async(card: Card) => {

        card.count ? card.count += 1 : card.count = 1

        const res = await addToCollection(card)
        const res2 = await removeFromWishlist(card)

        
    }

    const remove = async (card: Card) => {

        card.count ? card.count -= 1 : card.count = 0

        const res = await removeFromCollection(card)
        if (res?.msg === 'Success') return
        collection.value.splice(index, 0, copy)

    }

    const exists = (card: Card) => {
        collection.value.some(c => {
            return c.card_id === card.card_id
        })
    }

    const fetch = async(limit: number = 10, offset: number = 0, user_id?: string) => {
        const res = await fetchCollection(limit, offset, user_id)
        return res
    }
    return { add, remove, exists, fetch }
}