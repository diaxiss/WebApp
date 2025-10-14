import sqlite3


def get_user_info(id):
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

    query = '''
    SELECT name, email, picture
    FROM user
    WHERE id = ?
    '''

    result = cur.execute(query, [id]).fetchall()[0]
    return {'name': result[0], 'email': result[1], 'picture': result[2]}

def add_user_to_db(user: dict, con, cur):
    
    query = '''
    INSERT INTO user(google_id, email, name, picture)
    VALUES (?, ?, ?, ?)
    '''

    cur.execute(query, [user['sub'], user['email'], user['name'], user['picture']])



def check_user_in_db(user: dict) -> None:
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

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

    con = sqlite3.connect('../data/cards.db')
    cur = con.cursor()

    query = '''
    CREATE TABLE user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT UNIQUE NOT NULL,
        email TEXT,
        name TEXT,
        picture TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    '''
    cur.execute(query)

    query = '''
    CREATE TABLE wishlist(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_id TEXT NOT NULL,
        FOREIGN KEY (card_id) REFERENCES cards(id)
    )
    '''
    cur.execute(query)

    con.commit()