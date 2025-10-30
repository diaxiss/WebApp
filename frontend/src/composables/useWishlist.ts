import { wishlist } from "../utilities/constants";
import { addToWishlist, fetchWishlist, removeFromWishlist } from "../utilities/wishlist";

import type { Card } from "../utilities/interfaces";


export function useWishlist(){

    const add = async (card: Card) => {
        wishlist.value.push(card)
        const res = await addToWishlist(card)
        if (res?.msg !== 'Success') wishlist.value.pop()
    };

    const remove = async (card: Card) => {
        const index = wishlist.value.findIndex(c => {
            return c.card_id === card.card_id
        })
        if (index === -1) return;
        const copy = {...wishlist.value[index]} as Card
        wishlist.value.splice(index, 1)

        const res = await removeFromWishlist(card);
        if (res?.msg !== 'Success') wishlist.value.splice(index, 0, copy)
    };

    const exists = (card: Card) => {
        wishlist.value.some(c => c.card_id === card.card_id)
    }

    const fetch = async() => {
        const res = await fetchWishlist()
        wishlist.value = res.wishlist
        return res.wishlist
    }

    return {wishlist, add, remove, exists, fetch}
}