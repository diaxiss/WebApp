from tcgdexsdk import TCGdex, Query
from tcgdexsdk.enums import Extension, Quality
import sqlite3
import requests
import asyncio
from tcgdexsdk.models.Card import Card
from tcgdexsdk.models.Set import Set
from tcgdexsdk.models.SetResume import SetResume

tcgdex = TCGdex()

async def save_image(path: str, content: bytes):
    
    def write_file():
        with open(path, 'wb') as f:
            f.write(content)
            f.flush()


    await asyncio.to_thread(write_file)


async def fetch_logo(set_item):
    logo = set_item.get_logo(Extension.PNG)
    if logo is not None:
        content = await asyncio.to_thread(logo.read)
        await save_image(f'../data/set_logo/{set_item.id}.png', content)


async def fetch_symbol(set_item):
    symbol = set_item.get_symbol(Extension.PNG)
    if symbol is not None:
        content = await asyncio.to_thread(symbol.read)
        await save_image(f'../data/set_symbol/{set_item.id}.png', content)


async def process_set_images(set_item):

    await asyncio.gather(
        fetch_logo(set_item),
        fetch_symbol(set_item)
    )

async def fetch_set_details_concurr():
    sets = await tcgdex.set.list()

    tasks = [asyncio.create_task(process_set_images(set_item)) for set_item in sets]
    await asyncio.gather(*tasks)

asyncio.run(fetch_set_details_concurr())