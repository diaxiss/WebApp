import sqlite3


def get_all_sets() -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT DISTINCT card_sets.name
    FROM card_sets
    ORDER BY card_sets.release_date ASC
    '''
    
    result = [field[0] for field in cur.execute(query).fetchall()]
    con.close()
    return result


def get_all_rarities() -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT DISTINCT card.rarity
    FROM card
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
    '''

    result = [field[0] for field in cur.execute(query).fetchall()]
    con.close()
    return result


def formatQueryResult(queryResult: list) -> list:

    result = []
    keys = ['card_id', 'name', 'illustrator', 'rarity', 'card_set', 'release_date', 'image']

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

            case 'release_date':
                conditions.append(f"card_sets.release_date >= ?")
                values.append(value[0])
                conditions.append(f"card_sets.release_date <= ?")
                values.append(value[1])

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
    card_id: str = None,
    release_date: tuple = None
    ) -> list:

    params = {k: v for k, v in locals().items() if v is not None}

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT card.id, card.name, card.illustrator, card.rarity, card_sets.name, card_sets.release_date, card.image
    FROM card
    LEFT JOIN card_sets
    ON card.set_id = card_sets.id
    WHERE 
    '''

    conditions, values = parseConditions(params)
    query += ' AND '.join(conditions)
    query += ' LIMIT ? OFFSET ?'
    values.extend([limit, offset])

    result = cur.execute(query, values).fetchall()
    con.close()
    return formatQueryResult(result)


def get_all_cards(limit: int, offset: int) -> tuple:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT card.id, card.name, card.illustrator, card.rarity, card_sets.name, card_sets.release_date, card.image
    FROM card
    LEFT JOIN card_sets
    on card.set_id = card_sets.id
    ORDER BY release_date DESC, card.id ASC
    LIMIT ?
    OFFSET ?
    '''
    result = cur.execute(query, (limit, offset)).fetchall()

    numOfCards = '''
    SELECT COUNT(*) AS total_cards
    FROM card
    '''
    numOfCardsResult = cur.execute(numOfCards).fetchall()[0]

    con.close()
    return formatQueryResult(result), numOfCardsResult