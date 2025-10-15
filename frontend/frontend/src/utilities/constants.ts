import { reactive, ref, type Reactive } from "vue"
import type { SearchPayload } from './interfaces'
import { fetchImage } from "./aplFetch"

const limit = ref<number>(10)
const offset = ref<number>(0)

const name = ref<string | null>(null)
const illustrator = ref<string | null>(null)
const rarity = ref<string | null>(null)
const card_set = ref<string | null>(null)
const card_id = ref<string | null>(null)
const release_date_from = ref<string | null>(null)
const release_date_to = ref<string | null>(null)

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

export const numOfCards = ref<number>(0)
export const numOfPages = ref<number>(-1)
export const currentPage = ref<number>(1)


export const userName = ref<string | null>(localStorage.getItem('user'))
export const userPicture = ref<string | null>(
    await fetchImage(`${localStorage.getItem('image')}.png`, 'user_images')
)