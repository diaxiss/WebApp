from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from scripts.userDbQueries import get_user_info
from scripts.wishlistCollectionDb import remove_card_from_collection
from scripts.wishlistCollectionDb import add_card_to_collection, get_user_collection
from scripts.googleAuth import decode_token



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-google")


#------------------------------
# Models
#------------------------------
class CollectionRequest(BaseModel):
    card_id: str
    count: int


#--------------------------
# Routes
#--------------------------
@router.get('/collection')
async def fetch_user_collection(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_collection(sub)
        cards = result['cards']
        return {'cards': cards}
    return HTTPException


@router.get('/collection/summary')
async def fetch_user_collection(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_collection(sub, limit=10)
        cards = result['cards']
        return {'cards': cards}
    return HTTPException


@router.post('/collection')
async def add_to_collection(request: CollectionRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        add_card_to_collection(request.card_id, request.count, sub)
        return
    return HTTPException


@router.delete('/collection')
async def remove_from_collection(request: CollectionRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        remove_card_from_collection(request.card_id, request.count, sub)
        return
    return HTTPException