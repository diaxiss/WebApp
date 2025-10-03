import { ref } from "vue"
import type { SearchPayload } from "../components/Interfaces.vue";

const limit = ref<number>(10)
const offset = ref<number>(0)

const name = ref<string | null>()
const illustrator = ref<string | null>()
const rarity = ref<string | null>()
const card_set = ref<string | null>()
const card_id = ref<string | null>()
const release_date = ref<string | null>()

export const payload: SearchPayload={
    name: name.value,
    illustrator: illustrator.value,
    rarity: rarity.value,
    card_set: card_set.value,
    card_id: card_id.value,
    release_date: release_date.value,
    limit: limit.value,
    offset: offset.value,
};