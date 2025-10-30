from tcgdexsdk import TCGdex, Query
from tcgdexsdk.enums import Extension, Quality
import sqlite3
import requests
import asyncio
from tcgdexsdk.models.Card import Card
from tcgdexsdk.models.Set import Set
from tcgdexsdk.models.SetResume import SetResume


tcgdex = TCGdex()

def format_card(card: dict, card_set: Set) -> dict:

    card['set_id'] = card_set.id
    return card


def setExistsInDb(item: SetResume):
    con = sqlite3.connect('../data/cards.db')
    cur = con.cursor()
    name = str(item.name)
    name = f'{name}%'
    print(name)
    query = '''
    SELECT name
    FROM card_sets
    WHERE name LIKE ?
    '''
    result = cur.execute(query, [name]).fetchall()
    if len(result) == 0:
        return False
    return True


def addCardsToDb(cards: list) -> None:

    con = sqlite3.connect('../data/cards.db')
    cur = con.cursor()

    for card in cards:

        query = '''
        INSERT INTO card
        VALUES (?, ?, ?, ?, ?, ?)
        '''

        params = [card['id'], card['set_id'], card['name'], card['illustrator'], f'{card['id']}.png', card['rarity']]
        #print(params)
        cur.execute(query, params)

    con.commit()
    con.close()


def addSetToDb(card_set: Set) -> None:

    con = sqlite3.connect('../data/cards.db')
    cur = con.cursor()

    params = [card_set.id, card_set.name, card_set.releaseDate, card_set.cardCount.total, card_set.cardCount.official] 
    #print(params)

    query = '''
    INSERT INTO card_sets
    VALUES(?, ?, ?, ?, ?)
    '''

    cur.execute(query, params)
    con.commit()
    con.close()


async def downloadImages(cards: list):

    for card in cards:

        image = card['image']
        if image == None:
            continue
        #print(image)
        response = requests.get(image)
        print(card)
        with open(f'../data/images/{card['id']}.png', 'wb') as out:
            out.write(response.content)

async def fetch_sets():
    
    allSets = {}

    sets = await tcgdex.set.list(Query().like("name", "Mega"))

    for item in sets:

        if setExistsInDb(item):
            continue

        card_set = await get_set(item.id)
        #print(card_set)
        addSetToDb(card_set)

        cards = []
        for card in card_set.cards:
            card = await fetch_card(card.id)
            card = format_card(card, card_set)
            cards.append(card)
            #print(card)

        await downloadImages(cards)
        addCardsToDb(cards)


async def get_set(id: str):
    card_set = await tcgdex.set.get(id)
    return card_set

async def get_cards_from_set(set: list):

    cards = {}

    for card in set['cards']:
        cardData = await fetch_card(card)
        cards[card] = cardData
    return cards

async def fetch_card(id: str = 'sv06-214'):
    
    card = await tcgdex.card.get(id)

    image = card.get_image_url(Quality.HIGH, Extension.PNG)

    return {'id': card.id, 'name': card.name, 'image': image, 'illustrator': card.illustrator,
                      'rarity': card.rarity}

#asyncio.run(fetch_sets())