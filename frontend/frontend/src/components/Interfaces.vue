<script lang="ts">

export interface SearchPayload{
    name?: string | null
    illustrator?: string | null
    rarity?: string | null
    card_set?: string | null
    card_id?: string | null
    release_date?: string | null
    limit: number,
    offset: number
}

export interface Card{
    name: string,
    illustrator: string,
    rarity: string,
    card_set: string,
    card_id: string, 
    release_date:string
    image: string | null
}

</script>