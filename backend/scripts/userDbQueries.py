import sqlite3

def initialize_db():
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()
    return con, cur

def get_user_collection(sub: str):
    con, cur = initialize_db()

    query = '''
    SELECT card_id
    FROM wishlist
    JOIN card
    ON wishlist.card_id = card.id
    JOIN card_sets
    ON card.set_id = card_sets.id 
    WHERE google_id = ?
    ORDER BY card_sets.release_date
    LIMIT 10
    '''
    result = cur.execute(query, [sub]).fetchall()
    
    return result

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
    return result[0][0]


def main():

    con, cur = initialize_db()

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

    query = '''
    CREATE TABLE wishlist(
        google_id TEXT NOT NULL,
        card_id TEXT NOT NULL,
        FOREIGN KEY (card_id) REFERENCES card(id),
        FOREIGN KEY (google_id) REFERENCES user(google_id)
    )
    '''
    cur.execute(query)

    con.commit()
main()