import sqlite3
import requests

def initialize_db():
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()
    return con, cur

def get_user_collection_or_wishlist(sub: str, col_or_wish = 'collection'):
    con, cur = initialize_db()

    baseQuery = f'''
    FROM {col_or_wish}
    JOIN card
    ON {col_or_wish}.card_id = card.id
    JOIN card_sets
    ON card.set_id = card_sets.id 
    WHERE google_id = ?
    ORDER BY card_sets.release_date
    '''
    cardQuery = f"SELECT card_id{', count' if col_or_wish == 'collection' else ' '} " + baseQuery + ' LIMIT 10' 
    cards = cur.execute(cardQuery, [sub]).fetchall()

    if col_or_wish == 'collection':
        for i, item in enumerate(cards):
            cards[i] = {'card_id': item[0], 'count': item[1]}
    else:
        for i, item in enumerate(cards):
            cards[i] = {'card_id': item[0]}
    
    totalCardQuery = 'SELECT COUNT(*) ' + baseQuery
    total_cards = cur.execute(totalCardQuery, [sub]).fetchall()[0]

    return {'cards': cards, 'numOfCards': total_cards}

def get_user_info(sub: str):
    con, cur = initialize_db()

    query = '''
    SELECT name, email, picture
    FROM user
    WHERE google_id = ?
    '''

    result = cur.execute(query, [sub]).fetchall()[0]
    return {'name': result[0], 'email': result[1], 'picture': result[2]}

def add_user_to_db(user: dict, con, cur):
    resultImage = requests.get(user['picture'])
    user['picture'] = f'{user["sub"]}.png'
    print(resultImage)
    with open(f'./data/user_images/{user["sub"]}.png', 'wb') as image:
        image.write(resultImage.content)
    query = '''
    INSERT INTO user(google_id, email, name, picture)
    VALUES (?, ?, ?, ?)
    '''

    cur.execute(query, [user['sub'], user['email'], user['name'], user['picture']])



def check_user_in_db(user: dict) -> None:
    con, cur = initialize_db()

    query = '''
    SELECT id
    FROM user
    WHERE google_id = ?
    '''

    result = cur.execute(query, [user['sub']]).fetchall()
    if len(result) == 0:
        add_user_to_db(user, con, cur)
        con.commit()
    result = cur.execute(query, [user['sub']]).fetchall()
    return result[0][0]


def main():

    con = sqlite3.connect('../data/cards.db')
    cur = con.cursor()

    # query = '''
    # CREATE TABLE user(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     google_id TEXT UNIQUE NOT NULL,
    #     email TEXT,
    #     name TEXT,
    #     picture TEXT,
    #     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    #     updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    # )
    # '''
    # cur.execute(query)

    cur.execute('DROP TABLE wishlist')
    cur.execute('DROP TABLE collection')

    query = '''
    CREATE TABLE wishlist(
        google_id TEXT NOT NULL,
        card_id TEXT NOT NULL,
        FOREIGN KEY (card_id) REFERENCES card(id) ON DELETE CASCADE,
        FOREIGN KEY (google_id) REFERENCES user(google_id) ON DELETE CASCADE,
        PRIMARY KEY (google_id, card_id)
    )
    '''
    cur.execute(query)
    query = '''
    CREATE TABLE collection(
        google_id TEXT NOT NULL,
        card_id TEXT NOT NULL,
        count INTEGER NOT NULL,
        FOREIGN KEY (card_id) REFERENCES card(id) ON DELETE CASCADE,
        FOREIGN KEY (google_id) REFERENCES user(google_id) ON DELETE CASCADE,
        PRIMARY KEY (google_id, card_id)
    )
    '''
    cur.execute(query)

    query = """
    INSERT INTO collection
    VALUES('105057099070763030387', 'me01-187', 1)
    """
    cur.execute(query)
    con.commit()