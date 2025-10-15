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