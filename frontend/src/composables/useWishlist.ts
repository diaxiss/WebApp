import { addToWishlist, fetchWishlist, removeFromWishlist } from "../utilities/wishlist";

import type { Card } from "../utilities/interfaces";
import type { Ref } from "vue";


export function useWishlist(cards: Ref<Card[]>){

    const add = async (card: Card) => {
        
        card.in_wishlist = true
        const res = await addToWishlist(card)
        if (res?.msg !== 'Success') card.in_wishlist = false
    };

    const remove = async (card: Card) => {

        card.in_wishlist = false

        const res = await removeFromWishlist(card);
        if (res?.msg !== 'Success') 
            card.in_wishlist = true
    };

    const exists = (card: Card) => {
        return cards.value.some(c => c.card_id === card.card_id)
    }

    const fetch = async(limit: number = 10, offset: number = 0, user_id?: string) => {
        return await fetchWishlist(limit, offset, user_id)
    }

    return {add, remove, exists, fetch}
}