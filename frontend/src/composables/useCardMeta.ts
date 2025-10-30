import type { Ref } from "vue";
import { onMounted, ref } from 'vue';
import { fetchAllIllustrators, fetchAllRarities, fetchAllSetsInfo } from "../utilities/aplFetch";

export function useCardMeta() {
    const allSets: Ref<String[]> = ref<String[]>([]);
    const allRarities: Ref<String[]> = ref<String[]>([]);
    const allIllustrators: Ref<String[]> = ref<String[]>([]);

    onMounted(async() => {
        allSets.value = await fetchAllSetsInfo()
        allRarities.value = await fetchAllRarities()
        allIllustrators.value = await fetchAllIllustrators()
    });
    return {allSets, allRarities, allIllustrators}
}