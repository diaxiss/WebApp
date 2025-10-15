#------------------
# STDLIB libraries
#------------------
import sys
import requests
sys.path.insert(1, './scripts')

#-----------------------
# Third party libraries
#-----------------------
from typing import Annotated
from fastapi import FastAPI, Response, Depends, Cookie
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

#-----------------
# Local packages
#-----------------
from scripts.googleAuth import handle_google_authentification, decode_token, create_access_token

from dbQueries import get_all_rarities, get_all_cards, get_all_sets, get_all_sets_info, get_all_illustrators
from dbQueries import query_card

from wishlistCollectionDb import add_card_to_wishlist, add_card_to_collection
from wishlistCollectionDb import remove_card_from_collection, remove_card_from_wishlist

from userDbQueries import get_user_info, get_user_collection_or_wishlist


#-----------
# App setup
#-----------

app = FastAPI()

#serve images
app.mount('/images', StaticFiles(directory='./data/images'), name = 'images')
app.mount('/user_images', StaticFiles(directory='./data/user_images'), name = 'user_images')

# Allow requests from frontend
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
]

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# authentification scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-google")



#-------------
# Models
#-------------

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

class AuthRequest(BaseModel):
    credential: str

class WishlistRequest(BaseModel):
    card_id: str

class CollectionRequest(BaseModel):
    card_id: str
    count: int

class Cookies(BaseModel):
    refresh_token: str


#----------------------------------
# GET all routes
#----------------------------------

@app.get('/rarities/info')
async def get_rarities():
    result = get_all_rarities()
    return {"rarities": result}

@app.get('/sets/info')
async def get_sets():
    result = get_all_sets_info()
    return {'sets': result}

@app.get('/sets')
async def get_sets():
    result = get_all_sets()
    return {'sets': result}

@app.get('/illustrators/info')
async def get_illustrators():
    result = get_all_illustrators()
    return {'illustrators': result}



#----------------------------------------
# GET with parameters
#----------------------------------------

@app.get('/card/{card_id}')
async def get_item(card_id: str):
    return {"card": f'{card_id}'}



@app.get('/sets/{set_id}')
async def get_set(set_id: str):
    result, _ = query_card(card_set_id = set_id, limit = 500, offset = 0)
    return {"cards": result}



#----------------
# POST queries
#----------------

@app.post('/search')
async def search(request: SearchRequest):

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



@app.post('/cards')
async def get_all_items(request: CardsRequest):
    result, numOfCards = get_all_cards(request.limit, request.offset)
    return {"cards": result, 'numOfCards': numOfCards}



#----------------------------------------
# Google authentification and user info
#----------------------------------------

@app.post('/auth-google')
async def handle_authentification_request(request: AuthRequest, response: Response) -> dict:
    user, email, picture, access_token, refresh_token = handle_google_authentification(request.credential)
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,           # must be True in production (HTTPS)
        samesite="none"        # allow cross-site requests
    )
    return {'user': {'name': user, 'picture': picture, 'email': email}, 'access_token': access_token}

@app.get('/user')
async def fetch_user_info(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_info(sub)
        return result
    return HTTPException

@app.post('/logout')
async def handle_logout(response: Response):
    response.delete_cookie(
        key='refresh_token',
        path='/',
        httponly=True,
        secure=True,
        samesite='none'
    )
    return {'msg': 'Logged out'}

@app.post('/refresh-token')
async def refresh_access_token(cookies: Annotated[Cookies, Cookie()]):

    refresh_token=cookies.refresh_token
    decoded_refresh_token = decode_token(refresh_token)

    if decoded_refresh_token:
        del decoded_refresh_token['exp']
        newAccessToken = create_access_token(decoded_refresh_token)
        return {'access_token': newAccessToken}

#--------------------------------
# Wishlist and Collection routes
#--------------------------------
@app.get('/wishlist')
async def fetch_user_wishlist(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_collection_or_wishlist(sub, 'wishlist')
        cards = result['cards']
        numOfCards = result['numOfCards']
        return {'cards': cards, 'numOfCards': numOfCards}
    return HTTPException

@app.post('/wishlist')
async def add_to_wishlist(request: WishlistRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        add_card_to_wishlist(request.card_id, sub)
        return
    return HTTPException

@app.delete('/wishlist')
async def remove_from_wishlist(request: WishlistRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        remove_card_from_wishlist(request.card_id, sub)
        return
    return HTTPException


@app.get('/collection')
async def fetch_user_collection(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_collection_or_wishlist(sub, 'collection')
        cards = result['cards']
        numOfCards = result['numOfCards']
        return {'cards': cards, 'numOfCards': numOfCards}
    return HTTPException

@app.post('/collection')
async def add_to_collection(request: CollectionRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        add_card_to_collection(request.card_id, request.count, sub)
        return
    return HTTPException

@app.delete('/collection')
async def remove_from_collection(request: CollectionRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        remove_card_from_collection(request.card_id, request.count, sub)
        return
    return HTTPException