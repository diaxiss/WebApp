import sqlite3

con = sqlite3.connect('../data/cards.db')
cur = con.cursor()


def create_card():
    cur.execute('DROP TABLE IF EXISTS card')
    cur.execute('''
        CREATE TABLE card (
        id VARCHAR(16) PRIMARY KEY,
        set_id VARCHAR(16),
        name VARCHAR(64) NOT NULL,
        illustrator VARCHAR(64),
        rarity VARCHAR(64),
        FOREIGN KEY (set_id) REFERENCES card_sets (id)
        )
    ''')

def create_sets():
    cur.execute('DROP TABLE IF EXISTS card_sets')
    cur.execute('''
        CREATE TABLE card_sets (
        id VARCHAR(16) PRIMARY KEY,
        name VARCHAR(64),
        release_date VARCHAR(10),
        card_count_total INTEGER,
        card_count_official INTEGER,
        tcgpocket INTEGER
        )
    ''')

def create_user():
    cur.execute('DROP TABLE IF EXISTS user')

    # query= '''
    # DELETE FROM sqlite_sequence
    # WHERE name='user';
    # '''
    # cur.execute(query)

    cur.execute('''
        CREATE TABLE user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            google_id TEXT UNIQUE NOT NULL,
            email TEXT,
            name TEXT,
            picture TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            public BOOL DEFAULT 1
        )
        ''')


def create_wishlist():
    cur.execute('DROP TABLE IF EXISTS wishlist')
    cur.execute('''
        CREATE TABLE wishlist(
            google_id TEXT NOT NULL,
            card_id TEXT NOT NULL,
            FOREIGN KEY (card_id) REFERENCES card(id) ON DELETE CASCADE,
            FOREIGN KEY (google_id) REFERENCES user(google_id) ON DELETE CASCADE,
            PRIMARY KEY (google_id, card_id)
        )
        ''')


def create_collection():
    cur.execute('DROP TABLE IF EXISTS collection')
    cur.execute('''
        CREATE TABLE collection(
            google_id TEXT NOT NULL,
            card_id TEXT NOT NULL,
            count INTEGER NOT NULL,
            FOREIGN KEY (card_id) REFERENCES card(id) ON DELETE CASCADE,
            FOREIGN KEY (google_id) REFERENCES user(google_id) ON DELETE CASCADE,
            PRIMARY KEY (google_id, card_id)
        )
        ''')

# create_card()
# create_sets()

create_user()
create_collection()
create_wishlist()



con.commit()