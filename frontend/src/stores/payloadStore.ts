import { defineStore } from "pinia";
import { reactive } from "vue";
import type { SearchPayload } from "../utilities/interfaces";

export const usePayloadStore = defineStore('payload', () => {

    const payload = reactive<SearchPayload>({
        name: null,
        illustrator:null,
        rarity: null,
        card_set: null,
        card_id: null,
        release_date_from: null,
        release_date_to: null,
        limit: 10,
        offset: 0,
    })

    function clearPayload() {

        payload.name = null
        payload.illustrator = null
        payload.rarity = null
        payload.card_set = null
        payload.card_id = null
        payload.release_date_from = null
        payload.release_date_to = null

    }

    return {payload, clearPayload}
})