from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import datetime
from userDbQueries import check_user_in_db
from fastapi import HTTPException, status
from env import GOOGLE_CLIENT_ID


SECRET_KEY = 'random_string_to_protect_pokemon_data'
ALGORITHM = "HS256"


def create_access_token(user: dict, expires_minutes: int = 15) -> str:
    to_encode = user.copy()
    now = datetime.datetime.now(datetime.UTC)
    expire = now + datetime.timedelta(minutes=expires_minutes)
    to_encode.update({'exp': expire, 'iat': now})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )



def create_refresh_token(user: dict, expires_delta: int = 60*60*24*7):
    to_encode = user.copy()
    now = datetime.datetime.now(datetime.UTC)
    expire = now + datetime.timedelta(minutes=expires_delta)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_google_token(credential):
    try:
        
        idInfo = id_token.verify_oauth2_token(
            credential,
            requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=5
        )
        return idInfo

    except ValueError as e:
        print(e)
        return None


def handle_google_authentification(credential):
    
    idInfo = verify_google_token(credential)

    if not idInfo:
        raise HTTPException(status_code=400, detail="Invalid Google token")

    user = {
        'sub': idInfo['sub'],
        'email': idInfo['email'], 
        'name': idInfo['name'],
        'picture': idInfo['picture']
    }

    check_user_in_db(user)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return [user['name'], user['email'], user['sub'], access_token, refresh_token]
    