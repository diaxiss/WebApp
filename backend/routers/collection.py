from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from scripts.userDbQueries import get_user_info
from scripts.wishlistCollectionDb import remove_card_from_collection
from scripts.wishlistCollectionDb import add_card_to_collection, get_user_collection
from scripts.googleAuth import decode_token



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-google")

class CollectionRequest(BaseModel):
    card_id: str

#--------------------------
# Routes
#--------------------------
@router.get('/collection')
def fetch_user_collection(limit: int = 10, offset: int = 0, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_collection(sub=sub, viewer=sub, limit=limit)
        cards = result['cards']
        return {'cards': cards}
    return HTTPException


@router.post('/collection')
def add_to_collection(request: CollectionRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        add_card_to_collection(request.card_id, sub)
        return
    return HTTPException



#-------------------------------
# User queries
#------------------------------- 

@router.get('/collection/user{id}')
def fetch_user_collection_id(id: str, limit: int = 10, offset: int = 0, self = False):
    result = get_user_collection(user_id)
    cards = result['cards']
    return {'cards': cards}

@router.delete('/collection/{card_id}')
def remove_from_collection(card_id: str, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        remove_card_from_collection(card_id, sub)
        return
    return HTTPException