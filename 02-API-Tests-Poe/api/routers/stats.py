from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends  
from sqlalchemy import func, select  
from sqlalchemy.orm import Session

from api.schemas import GenreStats  
from database.db import get_db  
from database.models import Game

router = APIRouter(prefix="/stats", tags=["stats"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/overview")  
def overview(db: DbSession):  
    row = db.execute(  
        select(  
            func.count().label("total_games"),  
            func.count(Game.critic_score).label("with_score"),  
            func.sum(Game.total_sales).label("total_sales"),  
            func.min(Game.release_date).label("earliest"),  
            func.max(Game.release_date).label("latest"),  
        )  
    ).one()  
    return {  
        "total_games": row.total_games,  
        "games_with_critic_score": row.with_score,  
        "total_sales_millions": round(row.total_sales or 0, 2),  
        "earliest_release": row.earliest,  
        "latest_release": row.latest,  
    }


@router.get("/sales-by-genre", response_model=List[GenreStats])  
def sales_by_genre(db: DbSession):  
    rows = db.execute(  
        select(  
            Game.genre,  
            func.count().label("game_count"),  
            func.sum(Game.total_sales).label("total_sales"),  
            func.avg(Game.critic_score).label("avg_critic_score"),  
        )  
        .group_by(Game.genre)  
        .order_by(func.sum(Game.total_sales).desc().nullslast())  
    ).all()  
    return [  
        GenreStats(  
            genre=r.genre,  
            game_count=r.game_count,  
            total_sales=round(r.total_sales, 2) if r.total_sales else None,  
            avg_critic_score=round(r.avg_critic_score, 2)  
            if r.avg_critic_score  
            else None,  
        )  
        for r in rows  
    ]  