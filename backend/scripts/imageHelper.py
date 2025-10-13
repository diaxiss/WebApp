import sqlite3
import os


def main():

    conn = sqlite3.connect('../data/cards.db')
    cur = conn.cursor()    

    for file in os.listdir('../data/images'):
        if not file.endswith('.png'):
            continue
        card_id = os.path.splitext(file)[0]
        print(card_id)
        
        cur.execute(
            "UPDATE card SET image = ? WHERE id = ? and image IS NOT NULL", (file, card_id)
        )
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()