from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy import func, nullslast, select  
from sqlalchemy.orm import Session

from api.dependencies import GameFilters, Paging, Sorting  
from api.schemas import GameOut, GamePage  
from database.db import get_db  
from database.models import Game

router = APIRouter(prefix="/games", tags=["games"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=GamePage)  
def list_games(  
    db: DbSession,  
    filters: GameFilters,  
    paging: Paging,  
    sorting: Sorting,  
):  
    col, order = sorting  
    ordering = nullslast(col.desc() if order == "desc" else col.asc())

    total_result = db.scalar(select(func.count()).select_from(Game).where(*filters))
    total = total_result if total_result is not None else 0

    games = db.scalars(  
        select(Game)  
        .where(*filters)  
        .order_by(ordering, Game.id)  
        .limit(paging.limit)  
        .offset(paging.offset)  
    ).all()

    items = [GameOut.model_validate(game) for game in games]

    return GamePage(  
        items=items, total=total, limit=paging.limit, offset=paging.offset  
    )


@router.get(  
    "/{game_id}",  
    response_model=GameOut,  
    responses={404: {"description": "Game not found"}},  
)  
def get_game(game_id: int, db: DbSession):  
    game = db.get(Game, game_id)  
    if game is None:  
        raise HTTPException(status_code=404, detail="Game not found")  
    return game  