from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from scripts.googleAuth import decode_token
from scripts.userDbQueries import get_user_info
from scripts.wishlistCollectionDb import add_card_to_wishlist, add_card_to_collection
from scripts.wishlistCollectionDb import remove_card_from_wishlist, get_user_wishlist

router = APIRouter()

# authentification scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-google")

#------------------------------
# Models
#------------------------------
class WishlistRequest(BaseModel):
    card_id: str


#--------------------------
# Routes
#--------------------------
@router.get('/wishlist')
def fetch_user_wishlist(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_wishlist(sub)
        cards = result['cards']
        return {'cards': cards}
    return HTTPException


@router.get('/wishlist/summary')
def fetch_user_wishlist(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_wishlist(sub, limit=10)
        cards = result['cards']
        return {'cards': cards}
    return HTTPException


@router.post('/wishlist')
def add_to_wishlist(request: WishlistRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        add_card_to_wishlist(request.card_id, sub)
        return
    return HTTPException


@router.delete('/wishlist')
def remove_from_wishlist(request: WishlistRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        remove_card_from_wishlist(request.card_id, sub)
        return
    return HTTPException