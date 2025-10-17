import { addToCollection, fetchCollection, removeFromCollection } from "../utilities/collection"
import { collection, wishlist } from "../utilities/constants"
import type { Card } from "../utilities/interfaces"
import { removeFromWishlist } from "../utilities/wishlist"


export function useCollection() {
    const add = async(card: Card) => {

        const wishlistIndex = wishlist.value.findIndex(c => {
            return c.card_id === card.card_id
        })

        if (wishlistIndex !== 1) wishlist.value.splice(wishlistIndex, 1)

        const index = collection.value.findIndex(c => {
            return c.card_id === card.card_id
        })
        if (index !== -1 && collection.value[index]?.count){
            collection.value[index].count+=1
        }else{
            collection.value.push({...card, count: 1});
        }

        const res = await addToCollection(card)
        const res2 = await removeFromWishlist(card)
        if (res?.msg !== 'Success' && res2?.msg !== 'Success'){
            if (index !== 1 && collection.value[index]?.count && collection.value[index].count > 1){
                collection.value[index].count -= 1;
            }else{
                collection.value.pop()
                if (wishlistIndex !== 1) wishlist.value.splice(wishlistIndex, 0, card)
            }
        }
    }

    const remove = async (card: Card) => {
        const index = collection.value.findIndex(c => {
            return c.card_id === card.card_id
        })
        if (index === -1) return
        const copy = {...collection.value[index]} as Card
        if (collection.value[index]?.count){
            collection.value[index].count -= 1
            if (collection.value[index].count < 1)
                collection.value.splice(index, 1)
        }

        const res = await removeFromCollection(card)
        if (res?.msg === 'Success') return
        collection.value.splice(index, 0, copy)

    }

    const exists = (card: Card) => {
        collection.value.some(c => {
            return c.card_id === card.card_id
        })
    }

    const fetch = async() => {
        const res = await fetchCollection()
        collection.value = res.collection
        return res.collection
    }
    return {collection, add, remove, exists, fetch }
}