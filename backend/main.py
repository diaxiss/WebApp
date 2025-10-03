from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dbUtil import query_card, get_all_rarities, get_all_cards, get_all_sets, get_all_illustrators
from fastapi.staticfiles import StaticFiles


app = FastAPI()

#serve images
app.mount('/images', StaticFiles(directory='./data/images'), name = 'images')

# Allow requests from frontend
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {"message": "Hello"}

@app.get('/card/{card_id}')
async def get_item(card_id: str):
    return {"card": f'{card_id}'}

@app.get('/rarities')
async def get_rarities():
    result = get_all_rarities()
    return {"rarities": result}

@app.get('/sets')
async def get_sets():
    result = get_all_sets()
    return {'sets': result}

@app.get('/illustrators')
async def get_illustrators():
    result = get_all_illustrators()
    return {'illustrators': result}

class SearchRequest(BaseModel):
    name: str = None
    illustrator: str = None
    rarity: str = None
    card_set: str = None
    card_id: str = None
    release_date: tuple = None
    limit: int = 10
    offset: int = 0


@app.post('/search')
async def search(request: SearchRequest):

    result = query_card(
        name = request.name,
        illustrator = request.illustrator,
        rarity = request.rarity,
        card_set = request.card_set,
        card_id = request.card_id,
        release_date = request.release_date,
        limit = request.limit,
        offset = request.offset
        )

    return {"message": "Success!", "data": result} 

class CardsRequest(BaseModel):
    limit: int
    offset: int

@app.post('/cards')
async def get_all_items(request: CardsRequest):
    result, numOfCards = get_all_cards(request.limit, request.offset)
    return {"cards": result, 'numOfCards': numOfCards}