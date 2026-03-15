import type { Ref } from "vue"
import { addToCollection, fetchCollection, removeFromCollection } from "../utilities/collection"
import type { Card } from "../utilities/interfaces"
import { removeFromWishlist } from "../utilities/wishlist"


export function useCollection(collection: Ref<Card[]>) {
    const add = async(card: Card) => {

        card.count ? card.count += 1 : card.count = 1

        await addToCollection(card)
        await removeFromWishlist(card)

        
    }

    const remove = async (card: Card) => {

        card.count ? card.count -= 1 : card.count = 0

        await removeFromCollection(card)

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