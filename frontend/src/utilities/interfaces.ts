export interface SearchPayload{
    name?: string | null
    illustrator?: string | null
    rarity?: string | null
    card_set?: string | null
    card_id?: string | null
    release_date_from?: string | null
    release_date_to?: string | null
    limit: number,
    offset: number
}

export interface Card{
    name: string,
    illustrator: string,
    rarity: string,
    card_set: string,
    card_set_id: string,
    card_id: string, 
    release_date:string,
    image: string | null,
    count?: number
}

export interface SetCard{
    id: string,
    name: string,
    release_date: string,
    card_count_official: string,
    card_count_total: string
}