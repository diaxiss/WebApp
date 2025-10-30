from fastapi import APIRouter
from pydantic import BaseModel

from scripts.dbQueries import get_all_rarities, get_all_illustrators
from scripts.dbQueries import get_all_sets, get_all_sets_info
from scripts.dbQueries import get_all_cards, query_card


router = APIRouter()

#-----------------------------------
# Models
#-----------------------------------

class SearchRequest(BaseModel):
    name: str = None
    illustrator: str = None
    rarity: str = None
    card_set: str = None
    card_set_id: str = None
    card_id: str = None
    release_date_from: str = None
    release_date_to: str = None
    limit: int = 10
    offset: int = 0
    
class CardsRequest(BaseModel):
    limit: int
    offset: int

#----------------------------------
# GET all routes
#----------------------------------

@router.get('/rarities/info')
def get_rarities():
    result = get_all_rarities()
    return {"rarities": result}

@router.get('/sets/info')
def get_sets():
    result = get_all_sets_info()
    return {'sets': result}

@router.get('/sets')
def get_sets():
    result = get_all_sets()
    return {'sets': result}

@router.get('/illustrators/info')
def get_illustrators():
    result = get_all_illustrators()
    return {'illustrators': result}

@router.get('/cards')
def get_cards():
    result, numOfCards = get_all_cards(limit = 100000)
    return {'numOfCards': numOfCards, 'cards': result, }

#----------------------------------------
# GET with parameters
#----------------------------------------

@router.get('/card/{card_id}')
def get_item(card_id: str):
    return {"card": f'{card_id}'}



@router.get('/sets/{set_id}')
def get_set(set_id: str):
    result, _ = query_card(card_set_id = set_id, limit = 500, offset = 0)
    return {"cards": result}


#--------------------------------------
# POST queries
#--------------------------------------

@router.post('/search')
def search(request: SearchRequest):

    result, numOfCards = query_card(
        name = request.name,
        illustrator = request.illustrator,
        rarity = request.rarity,
        card_set = request.card_set,
        card_set_id = request.card_set_id,
        card_id = request.card_id,
        release_date_from = request.release_date_from,
        release_date_to = request.release_date_to,
        limit = request.limit,
        offset = request.offset
        )

    return {"data": result,  'numOfCards': numOfCards} 

@router.post('/cards')
def get_all_items_limit(request: CardsRequest):
    result, numOfCards = get_all_cards(request.limit, request.offset)
    return {"cards": result, 'numOfCards': numOfCards}