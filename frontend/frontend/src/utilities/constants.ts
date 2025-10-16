import { reactive, ref, type Reactive } from "vue"
import type { Card, SearchPayload } from './interfaces'

//----------------------
// Card query parameters
//----------------------
const limit = ref<number>(10)
const offset = ref<number>(0)

const name = ref<string | null>(null)
const illustrator = ref<string | null>(null)
const rarity = ref<string | null>(null)
const card_set = ref<string | null>(null)
const card_id = ref<string | null>(null)
const release_date_from = ref<string | null>(null)
const release_date_to = ref<string | null>(null)

// Card query payload
export const payload: Reactive<SearchPayload>= reactive<SearchPayload>({
    name: name.value,
    illustrator: illustrator.value,
    rarity: rarity.value,
    card_set: card_set.value,
    card_id: card_id.value,
    release_date_from: release_date_from.value,
    release_date_to: release_date_to.value,
    limit: limit.value,
    offset: offset.value,
});


//------------------
// Pagination
//------------------
export const numOfCards = ref<number>(0)
export const numOfPages = ref<number>(-1)
export const currentPage = ref<number>(1)


//----------------------------------
// User data and authentification
//----------------------------------
export const accessToken = ref(localStorage.getItem('accessToken'))

export const userName = ref<string | null>(localStorage.getItem('user'))
export const userPicture = ref<string | null>(`http://localhost:8000/user_images/${localStorage.getItem('image')}.png`)
export const collection = ref<Card[]>([])
export const wishlist = ref<Card[]>([])