from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status  
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import CurrentUser, DbSession  
from api.schemas import Token, UserRead  
from core.security import create_access_token, decode_access_token, verify_password  
from database.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)  
def login(  
    form: Annotated[OAuth2PasswordRequestForm, Depends()],  
    db: DbSession,  
):  
    user = db.query(User).filter(User.username == form.username).first()  
    if not user or not verify_password(form.password, user.hashed_password):  
        raise HTTPException(  
            status_code=status.HTTP_401_UNAUTHORIZED,  
            detail="Incorrect username or password",  
            headers={"WWW-Authenticate": "Bearer"},  
        )  
    token = create_access_token(user.username)
    payload = decode_access_token(token)
    exp_timestamp = payload.get("exp")

    if not isinstance(exp_timestamp, (int, float)):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token was created without a valid expiration",
        )

    expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    expires_in = max(0, int((expires_at - datetime.now(timezone.utc)).total_seconds()))

    return Token(
        access_token=token,
        expires_in=expires_in,
        expires_at=expires_at,
    )


@router.get("/users/me", response_model=UserRead)  
def read_me(user: CurrentUser):  
    return user  