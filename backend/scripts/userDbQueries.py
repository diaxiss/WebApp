import sqlite3


def add_user_to_db(user: dict, con, cur):
    
    query = '''
    INSERT INTO user(google_id, email, name, picture)
    VALUES (?, ?, ?, ?)
    '''

    cur.execute(query, [user['sub'], user['email'], user['name'], user['picture']])



def check_user_in_db(user: dict) -> None:
    con = sqlite3.connect('./data/userDb.db')
    cur = con.cursor()

    query = '''
    SELECT google_id
    FROM user
    WHERE google_id = ?
    '''

    result = cur.execute(query, [user['sub']]).fetchall()
    if len(result) == 0:
        add_user_to_db(user, con, cur)
        con.commit()


def main():

    con = sqlite3.connect('../data/userDb.db')
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

    con.commit()


if __name__ == '__main__':
    main()