import sqlite3

def add_card_to_wishlist(card_id: str, sub: str) -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    INSERT INTO wishlist(google_id, card_id)
    VALUES(?, ?)
    ON CONFLICT (google_id, card_id) DO NOTHING
    '''
    
    cur.execute(query, [sub, card_id])

    con.commit()

def add_card_to_collection(card_id: str, count: int, sub: str) -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    INSERT INTO collection(google_id, card_id, count)
    VALUES(?, ?, ?)
    ON CONFLICT(google_id, card_id) DO
    UPDATE SET
    count = count + excluded.count
    '''
    
    cur.execute(query, [sub, card_id, count])

    con.commit()

def remove_card_from_collection(card_id: str, count: int, sub: str) -> None:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    cur.execute('''
        UPDATE collection
        SET count = count - ?
        WHERE google_id = ? and card_id = ?
    ''', [count, sub, card_id])

    query= '''
    DELETE FROM collection
    WHERE google_id = ? and card_id = ? AND count <= 0
    '''

    cur.execute(query, [sub, card_id])
    con.commit()

def remove_card_from_wishlist(card_id: str, sub: str) -> None:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query= '''
    DELETE FROM wishlist
    WHERE google_id = ? AND card_id = ?
    '''

    cur.execute(query, [sub, card_id])
    con.commit()

def get_user_collection(sub: str, limit: int = -1):
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    baseQuery = f'''
    FROM collection
    JOIN card
    ON collection.card_id = card.id
    JOIN card_sets
    ON card.set_id = card_sets.id 
    WHERE google_id = ?
    ORDER BY card_sets.release_date
    '''
    cards = cur.execute('SELECT card_id, count, card.name, card.image '+baseQuery+' LIMIT ?', [sub, limit]).fetchall()

    for i, item in enumerate(cards):
        cards[i] = {'card_id': item[0], 'count': item[1], 'name': item[2], 'image': item[3]}
    
    totalCardQuery = 'SELECT COUNT(*) ' + baseQuery
    total_cards = cur.execute(totalCardQuery, [sub]).fetchone()[0]

    return {'cards': cards, 'numOfCards': total_cards}


def get_user_wishlist(sub: str, limit: int = -1):
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    baseQuery = f'''
    FROM wishlist
    JOIN card
    ON wishlist.card_id = card.id
    JOIN card_sets
    ON card.set_id = card_sets.id 
    WHERE google_id = ?
    ORDER BY card_sets.release_date
    '''
    cards = cur.execute('SELECT card_id, card.name, card.image '+baseQuery+' LIMIT ?', [sub, limit]).fetchall()

    for i, item in enumerate(cards):
        cards[i] = {'card_id': item[0], 'name': item[1], 'image': item[2]}
    
    totalCardQuery = 'SELECT COUNT(*) ' + baseQuery
    total_cards = cur.execute(totalCardQuery, [sub]).fetchone()[0]

    return {'cards': cards, 'numOfCards': total_cards}