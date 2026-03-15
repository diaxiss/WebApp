from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer

from typing import Optional


def optional_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    print(authorization)
    if authorization and authorization.startswith('Bearer '):
        return authorization[len('Bearer '):]
    return None