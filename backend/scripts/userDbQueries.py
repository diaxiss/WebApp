import sqlite3
import requests


def get_user_info(sub: str):
    con = sqlite3.connect('./data/cards.db')
    cur = con.cursor()

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
    result = cur.execute(query, [user['sub']]).fetchall()
    return result[0][0]