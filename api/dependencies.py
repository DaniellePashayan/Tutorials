from datetime import date  
from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer  
from sqlalchemy.orm import Session
import jwt

from database.models import Game, User
from core.security import decode_access_token  
from database.db import get_db  

SORT_COLUMNS = {  
    "title": Game.title,  
    "console": Game.console,  
    "genre": Game.genre,  
    "publisher": Game.publisher,  
    "critic_score": Game.critic_score,  
    "total_sales": Game.total_sales,  
    "na_sales": Game.na_sales,  
    "jp_sales": Game.jp_sales,  
    "pal_sales": Game.pal_sales,  
    "release_date": Game.release_date,  
}


def game_filters(  
    q: Annotated[Optional[str], Query(description="Substring match on title")] = None,  
    console: Annotated[Optional[List[str]], Query()] = None,  
    genre: Annotated[Optional[List[str]], Query()] = None,  
    publisher: Optional[str] = None,  
    developer: Optional[str] = None,  
    min_score: Annotated[Optional[float], Query(ge=0, le=10)] = None,  
    max_score: Annotated[Optional[float], Query(ge=0, le=10)] = None,  
    min_sales: Annotated[Optional[float], Query(ge=0)] = None,  
    released_after: Optional[date] = None,  
    released_before: Optional[date] = None,  
) -> list:  
    """Collect query params into a list of SQLAlchemy conditions."""  
    conditions = []  
    if q:  
        conditions.append(Game.title.ilike(f"%{q}%"))  
    if console:  
        conditions.append(Game.console.in_(console))  
    if genre:  
        conditions.append(Game.genre.in_(genre))  
    if publisher:  
        conditions.append(Game.publisher == publisher)  
    if developer:  
        conditions.append(Game.developer == developer)  
    if min_score is not None:  
        conditions.append(Game.critic_score >= min_score)  
    if max_score is not None:  
        conditions.append(Game.critic_score <= max_score)  
    if min_sales is not None:  
        conditions.append(Game.total_sales >= min_sales)  
    if released_after:  
        conditions.append(Game.release_date >= released_after)  
    if released_before:  
        conditions.append(Game.release_date <= released_before)  
    return conditions


class Pagination:  
    def __init__(  
        self,  
        limit: Annotated[int, Query(ge=1, le=100)] = 20,  
        offset: Annotated[int, Query(ge=0)] = 0,  
    ):  
        self.limit = limit  
        self.offset = offset


def sort_params(  
    sort: str = "total_sales",  
    order: Annotated[str, Query(pattern="^(asc|desc)$")] = "desc",  
):  
    if sort not in SORT_COLUMNS:  
        raise HTTPException(  
            status_code=400,  
            detail=f"sort must be one of: {', '.join(sorted(SORT_COLUMNS))}",  
        )  
    return SORT_COLUMNS[sort], order


# Reusable aliases so endpoint signatures stay readable  
GameFilters = Annotated[list, Depends(game_filters)]  
Paging = Annotated[Pagination, Depends()]  
Sorting = Annotated[tuple, Depends(sort_params)]  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(  
    token: Annotated[str, Depends(oauth2_scheme)],  
    db: DbSession,  
) -> User:  
    cred_error = HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED,  
        detail="Could not validate credentials",  
        headers={"WWW-Authenticate": "Bearer"},  
    )  
    try:  
        username = decode_access_token(token).get("sub")  
    except jwt.InvalidTokenError:   # type: ignore
        raise cred_error

    user = db.query(User).filter(User.username == username).first()  
    if user is None or user.disabled:  
        raise cred_error  
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]  