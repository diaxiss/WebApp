from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from typing import Optional

from scripts.googleAuth import decode_token
from scripts.userDbQueries import get_user_info
from scripts.wishlistCollectionDb import add_card_to_wishlist, add_card_to_collection
from scripts.wishlistCollectionDb import remove_card_from_wishlist, get_user_wishlist
from scripts.wishlistCollectionDb import wishlist_stats

router = APIRouter()

# authentification scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-google", auto_error=False)

class WishlistRequest(BaseModel):
    card_id: str

#--------------------------
# Routes
#--------------------------
@router.get('/wishlist')
def fetch_user_wishlist(limit: int = 10, offset: int = 0, token: str = Depends(oauth2_scheme)):
    print(limit, offset)
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_wishlist(sub=sub, self=True, viewer=sub, limit = limit, offset = offset)
        return {'cards': result['cards'], 'length': result['length']}
    return HTTPException


@router.post('/wishlist')
def add_to_wishlist(request: WishlistRequest, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        add_card_to_wishlist(request.card_id, sub)
        return
    return HTTPException


@router.delete('/wishlist/{card_id}')
def remove_from_wishlist(card_id: str, token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        remove_card_from_wishlist(card_id, sub)
        return
    return HTTPException

#-------------------------------
# User queries
#-------------------------------

@router.get('/wishlist/stats')
def wishlist_percentage(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        stats = wishlist_stats(sub)
        return {'stats': stats}
    return {'response': 'Error'}


@router.get('/wishlist/user/{id}')
def fetch_user_wishlist_id(id: str, limit: int = 10, offset: int = 0, token: Optional[str] = Depends(oauth2_scheme)):
    if token and token != "null":
        result = get_user_wishlist(sub=id, self=False, limit=limit, offset=offset, viewer = decode_token(token).get('sub'))
    else:
        result = get_user_wishlist(sub=id, self=False, limit=limit, offset=offset, viewer = None)
    return {'cards': result["cards"], 'length': result["length"]}
    