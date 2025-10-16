import sqlite3

con = sqlite3.connect('../data/cards.db')
cur = con.cursor()

#---------------------
# Rebuild user table
#---------------------
    # cur.execute('DROP TABLE user')

    # query= '''
    # DELETE FROM sqlite_sequence
    # WHERE name='user';
    # '''
    # cur.execute(query)
    # con.commit()

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

    # cur.execute('DROP TABLE wishlist')
    # query = '''
    # CREATE TABLE wishlist(
    #     google_id TEXT NOT NULL,
    #     card_id TEXT NOT NULL,
    #     FOREIGN KEY (card_id) REFERENCES card(id) ON DELETE CASCADE,
    #     FOREIGN KEY (google_id) REFERENCES user(google_id) ON DELETE CASCADE,
    #     PRIMARY KEY (google_id, card_id)
    # )
    # '''
    # cur.execute(query)

    # cur.execute('DROP TABLE collection')
    # query = '''
    # CREATE TABLE collection(
    #     google_id TEXT NOT NULL,
    #     card_id TEXT NOT NULL,
    #     count INTEGER NOT NULL,
    #     FOREIGN KEY (card_id) REFERENCES card(id) ON DELETE CASCADE,
    #     FOREIGN KEY (google_id) REFERENCES user(google_id) ON DELETE CASCADE,
    #     PRIMARY KEY (google_id, card_id)
    # )
    # '''
    # cur.execute(query)