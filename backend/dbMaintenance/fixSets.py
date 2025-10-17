from tcgdexsdk import TCGdex, Query
from tcgdexsdk.enums import Extension, Quality
import sqlite3
import requests
import asyncio
from tcgdexsdk.models.Card import Card
from tcgdexsdk.models.Set import Set
from tcgdexsdk.models.SetResume import SetResume

tcgdex = TCGdex()

async def fetch_sets():
    
    allSets = {}

    sets = await tcgdex.set.list()

    for item in sets:

        image = item.get_logo(Extension.PNG)
        if image != None:
            image = image.read()
            with open(f'../data/set_logo/{item.id}.png', 'wb') as output:
                output.write(image)
            
        image = item.get_symbol(Extension.PNG)
        if image != None:
            image = image.read()

            with open(f'../data/set_symbol/{item.id}.png', 'wb') as output:
                output.write(image)
                
asyncio.run(fetch_sets())