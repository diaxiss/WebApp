from fastapi import APIRouter
from fastapi import Response, Depends, Cookie
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from scripts.googleAuth import handle_google_authentification, decode_token, create_access_token
from scripts.userDbQueries import get_user_info
router = APIRouter()

# authentification scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth-google")


#----------------------------
# Models
#----------------------------
class AuthRequest(BaseModel):
    credential: str

class Cookies(BaseModel):
    refresh_token: str
    


#----------------------------------------
# Google authentification and user info
#----------------------------------------

@router.post('/auth-google')
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


@router.get('/user')
async def fetch_user_info(token: str = Depends(oauth2_scheme)):
    jwt_decoded = decode_token(token)
    if jwt_decoded:
        sub = jwt_decoded.get('sub')
        result = get_user_info(sub)
        return result
    return HTTPException


@router.post('/logout')
async def handle_logout(response: Response):
    response.delete_cookie(
        key='refresh_token',
        path='/',
        httponly=True,
        secure=True,
        samesite='none'
    )
    return {'msg': 'Logged out'}


@router.post('/refresh-token')
async def refresh_access_token(cookies: Annotated[Cookies, Cookie()]):
    
    refresh_token=cookies.refresh_token
    decoded_refresh_token = decode_token(refresh_token)

    if decoded_refresh_token:
        del decoded_refresh_token['exp']
        newAccessToken = create_access_token(decoded_refresh_token)
        return {'access_token': newAccessToken}
