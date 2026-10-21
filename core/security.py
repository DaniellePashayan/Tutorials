from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from core.config import get_settings

_hasher = PasswordHash.recommended()


def hash_password(raw: str) -> str:  
    return _hasher.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:  
    return _hasher.verify(raw, hashed)


def create_access_token(subject: str) -> str:  
    s = get_settings()  
    payload = {  
        "sub": subject,  
        "exp": datetime.now(timezone.utc)  
               + timedelta(minutes=s.access_token_ttl_minutes),  
    }  
    return jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_algorithm) # type: ignore


def decode_access_token(token: str) -> dict:  
    """Raises JWT decode errors on anything suspicious."""  
    s = get_settings()  
    return jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_algorithm])   # type: ignore