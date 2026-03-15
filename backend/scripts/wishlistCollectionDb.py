import sqlite3

#-----------------------------
# Wishlist
#-----------------------------

def get_user_wishlist(sub: str, viewer: str, self:bool = True, limit: int = -1, offset: int = 0):
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = f'''
    SELECT
        w.card_id,
        card.name,
        CASE WHEN wv.card_id IS NOT NULL
            THEN 1
            ELSE 0
        END AS in_wishlist,
        CASE WHEN col.card_id IS NOT NULL
            THEN col.count
            ELSE 0
        END as count
    FROM wishlist w
    JOIN card
        ON w.card_id = card.id
    JOIN card_sets
        ON card.set_id = card_sets.id 
    JOIN user
        ON w.google_id = user.google_id
    LEFT JOIN wishlist wv
        ON w.card_id = wv.card_id
        AND wv.google_id = ?
    LEFT JOIN collection col
        ON w.card_id = col.card_id
        AND col.google_id = ?
    WHERE w.google_id = ?
        {'' if self else 'AND user.public=1'}
    ORDER BY card_sets.release_date DESC, w.card_id
    LIMIT ?
    OFFSET ?
    '''
    cards = cur.execute(query, [viewer, sub, viewer, limit, offset]).fetchall()

    print(cards[1::3])

    for i, item in enumerate(cards):
        cards[i] = {'card_id': item[0], 'name': item[1], 'in_wishlist': item[2], 'count': item[3]}
    print(cards[1::3])
    return {'cards': cards, 
    'length': cur.execute('SELECT COUNT(*) FROM wishlist WHERE google_id = ?', [sub]).fetchone()[0]}


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


def remove_card_from_wishlist(card_id: str, sub: str) -> None:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query= '''
    DELETE FROM wishlist
    WHERE google_id = ? AND card_id = ?
    '''

    cur.execute(query, [sub, card_id])
    con.commit()



#-----------------------------
# Collection
#-----------------------------

def get_user_collection(sub: str, viewer: str, self:bool = True, limit: int = -1, offset: int = 0):

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = f'''
    SELECT
        col.card_id,
        card.name,
        count,
        CASE WHEN wv.card_id IS NOT NULL
            THEN 1
            ELSE 0
        END AS in_wishlist
    FROM collection AS col
    JOIN card
        ON col.card_id = card.id
    JOIN card_sets
        ON card.set_id = card_sets.id 
    JOIN user
        ON col.google_id = user.google_id
    LEFT JOIN wishlist wv
        ON col.card_id = wv.card_id
        AND wv.google_id = ?
    WHERE col.google_id = ? 
        {'' if self else 'AND user.public=1'}
    ORDER BY card_sets.release_date
    LIMIT ?
    OFFSET ?
    '''
    cards = cur.execute(query, [viewer, sub, limit, offset]).fetchall()

    for i, item in enumerate(cards):
        cards[i] = {'card_id': item[0], 'name': item[1], 'count': item[2], 'in_wishlist': item[3]}

    return {'cards': cards}

def add_card_to_collection(card_id: str, sub: str) -> list:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    INSERT INTO collection(google_id, card_id, count)
    VALUES(?, ?, 1)
    ON CONFLICT(google_id, card_id) DO
    UPDATE SET
    count = count + 1
    '''
    
    cur.execute(query, [sub, card_id])

    con.commit()

def remove_card_from_collection(card_id: str, sub: str) -> None:

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    cur.execute('''
        UPDATE collection
        SET count = count - 1
        WHERE google_id = ? and card_id = ?
    ''', [sub, card_id])

    query= '''
    DELETE FROM collection
    WHERE google_id = ? and card_id = ? AND count <= 0
    '''

    cur.execute(query, [sub, card_id])
    con.commit()


def wishlist_stats(sub: str):

    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    result = cur.execute('''
    SELECT 
        card_sets.name, 
        ROUND((1.0*COUNT(*) / card_count_total) * 100, 2) || '%' AS percent
    FROM wishlist
    JOIN card
        ON wishlist.card_id = card.id
    JOIN card_sets 
        ON card.set_id = card_sets.id
    GROUP BY card.set_id
    ORDER BY 1.0*COUNT(*)/card_count_total DESC
    ''').fetchall()

    for i, item in enumerate(result):
        result[i] = {'set': item[0], 'percentage_wishlisted': item[1]}

    return result

