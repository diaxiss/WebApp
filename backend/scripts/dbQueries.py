import sqlite3

def get_all_sets_info() -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT DISTINCT card_sets.name
    FROM card_sets
    WHERE tcgpocket = 0
    ORDER BY card_sets.release_date DESC
    '''
    
    result = [field[0] for field in cur.execute(query).fetchall()]

    con.close()
    return result


def get_all_sets() -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT DISTINCT id, name, release_date, card_count_official, card_count_total
    FROM card_sets
    WHERE tcgpocket = 0
    ORDER BY card_sets.release_date DESC
    '''
    
    result = cur.execute(query).fetchall()

    con.close()
    return formatQueryResult(result, ['id', 'name', 'release_date', 'card_count_official', 'card_count_total'])


def get_all_rarities() -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT DISTINCT card.rarity
    FROM card
    JOIN card_sets
    ON card.set_id = card_sets.id
    WHERE tcgpocket = 0
    ORDER BY card_sets.release_date DESC
    '''
    
    result = [field[0] for field in cur.execute(query).fetchall()]

    con.close()
    return result


def get_all_illustrators() -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT DISTINCT card.illustrator
    FROM card
    JOIN card_sets
    ON card.set_id = card_sets.id
    WHERE tcgpocket = 0
    '''

    result = [field[0] for field in cur.execute(query).fetchall()]

    con.close()
    return result


def formatQueryResult(queryResult: list, keys: list) -> list:

    result = []

    for item in queryResult:
        mapped = dict(zip(keys, item))
        result.append(mapped)

    return result


def parseConditions(params) -> tuple[list, list]:

    conditions = []
    values = []

    for param in params:

        value = params[param]
        if value == None:
            continue

        if param == 'card_id':
            param = 'id'

        match param:

            case 'name' | 'illustrator' | 'rarity' | 'card_id':
                conditions.append(f"LOWER(card.{param}) LIKE LOWER(?)")
                values.append(f'{value}%')

            case 'card_set':
                conditions.append(f"LOWER(card_sets.name) LIKE LOWER(?)")
                values.append(f'{value}%')
            
            case 'card_set_id':
                conditions.append(f"LOWER(card_sets.id) LIKE LOWER(?)")
                values.append(f'{value}')

            case 'release_date_from': 
                conditions.append(f"card_sets.release_date >= ?")
                values.append(f'{value}')

            case 'release_date_to':
                
                conditions.append(f"card_sets.release_date <= ?")
                values.append(f'{value}')

            case 'limit'| 'offset':
                pass

    return conditions, values


def query_card(
    limit: int,
    offset: int,
    name: str = None, 
    illustrator: str = None,
    rarity: str = None,
    card_set: str = None,
    card_set_id: str = None,
    card_id: str = None,
    release_date_from: str = None,
    release_date_to: str = None
    ) -> tuple[list, int]:

    params = {k: v for k, v in locals().items() if v is not None}

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT card.id, card.name, card.illustrator, card.rarity, card_sets.name, card_sets.id, card_sets.release_date, card.image, COUNT(*) OVER() as num_of_pages
    FROM card
    LEFT JOIN card_sets
    ON card.set_id = card_sets.id
    WHERE tcgpocket = 0 AND 
    '''

    conditions, values = parseConditions(params)

    query += ' AND '.join(conditions)
    query += ' ORDER BY card_sets.release_date DESC' 
    query += ' LIMIT ? OFFSET ?'

    values.extend([limit, offset])

    result = cur.execute(query, values).fetchall()

    if len(result) == 0:
        return [], 1

    numOfPages = result[0][-1]

    for item in result:
        item = item[:-1]

    con.close()
    return formatQueryResult(result, ['card_id', 'name', 'illustrator', 'rarity', 'card_set', 'card_set_id', 'release_date', 'image']), numOfPages


def get_all_cards(limit: int = 10, offset: int = 0) -> tuple[list, int]:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT card.id, card.name, card.illustrator, card.rarity, card_sets.name, card_sets.id, card_sets.release_date, card.image
    FROM card
    LEFT JOIN card_sets
    ON card.set_id = card_sets.id
    WHERE tcgpocket = 0
    ORDER BY release_date DESC, card.id ASC
    LIMIT ?
    OFFSET ?
    '''
    result = cur.execute(query, (limit, offset)).fetchall()

    numOfCards = '''
    SELECT COUNT(*) AS total_cards
    FROM card
    LEFT JOIN card_sets
    ON card.set_id = card_sets.id
    WHERE card_sets.tcgpocket = 0
    '''
    numOfCardsResult = cur.execute(numOfCards).fetchone()[0]

    con.close()
    return formatQueryResult(result, ['card_id', 'name', 'illustrator', 'rarity', 'card_set', 'card_set_id', 'release_date', 'image']), numOfCardsResult