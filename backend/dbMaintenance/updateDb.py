from tcgdexsdk import TCGdex, Query
from tcgdexsdk.enums import Extension, Quality
import sqlite3
import requests
import asyncio
from tcgdexsdk.models.Card import Card
from tcgdexsdk.models.Set import Set
from tcgdexsdk.models.SetResume import SetResume

import sys
import time

SET_CONCURRENCY = 25
set_semaphore = asyncio.Semaphore(SET_CONCURRENCY)

CARD_CONCURRENCY = 100
card_semaphore = asyncio.Semaphore(CARD_CONCURRENCY)

DOWNLOAD_CONCURRENCY = 100
download_semaphore = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)

DB_CONCURRENCY = 1
db_semaphore = asyncio.Semaphore(DB_CONCURRENCY)

# NUM_OF_LINES = 4


tcgdex = TCGdex()


def format_card(card: dict, card_set: Set) -> dict:

    card['set_id'] = card_set.id
    return card


def setExistsInDb(item: SetResume):
    con = sqlite3.connect('../data/cards.db')
    cur = con.cursor()
    query = '''
    SELECT name
    FROM card_sets
    WHERE name LIKE ?
    '''
    result = cur.execute(query, [f'{item.name}%']).fetchall()
    if len(result) == 0:
        return False
    return True


def addCardsToDb(cards: list) -> None:

    con = sqlite3.connect('../data/cards.db')
    cur = con.cursor()

    for card in cards:

        query = '''
        INSERT OR IGNORE INTO card
        VALUES (?, ?, ?, ?, ?)
        '''

        params = [card['id'], card['set_id'], card['name'], card['illustrator'], card['rarity']]
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
    INSERT OR IGNORE INTO card_sets
    VALUES(?, ?, ?, ?, ?, ?)
    '''

    cur.execute(query, params+[1 if card_set.id[0].isupper() else 0])
    con.commit()
    con.close()


def downloadImage(card: dict):


    print(f'Downloading images for {card['id']}',flush=True)

    image = card['image']
    if image is None:
        return
    #print(image)
    response = requests.get(image)
    with open(f'../data/images/{card['id']}.png', 'wb') as out:
        out.write(response.content)


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
    try:
        card = await tcgdex.card.get(id)

        image = card.get_image_url(Quality.HIGH, Extension.PNG)

        return {
            'id': card.id,
            'name': card.name,
            'image': image,
            'illustrator': card.illustrator,
            'rarity': card.rarity
        }

    except:
        return None



async def fetch_cards_concurr(card_set: Set):
    async def fetch_one(card):
        print(f'Fetching card: {card.id}', flush=True)
        async with card_semaphore:

            card = await fetch_card(card.id)
            if card is None:
                return None

            card = format_card(card, card_set)

            async with download_semaphore:
                await asyncio.to_thread(downloadImage, card)

            async with db_semaphore:
                await asyncio.to_thread(addCardsToDb, [card])

    tasks = [asyncio.create_task(fetch_one(card)) for card in card_set.cards]

    for task in asyncio.as_completed(tasks):
        card = await task
        if card is None:
            continue


async def process_set(item: SetResume):

    print(f'Set: {item.name}', flush=True)

    async with set_semaphore:

        if setExistsInDb(item):
            return

        card_set = await get_set(item.id)

        print(f'Adding {item.name} to db', flush=True)

        async with db_semaphore:
            await asyncio.to_thread(addSetToDb, card_set)

        await fetch_cards_concurr(card_set)



async def fetch_sets():
    
    allSets = {}

    sets = await tcgdex.set.list()


    tasks = [asyncio.create_task(process_set(item)) for item in sets]

    await asyncio.gather(*tasks)

asyncio.run(fetch_sets())