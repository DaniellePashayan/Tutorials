from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, Query  
from sqlalchemy import func, select  
from sqlalchemy.orm import InstrumentedAttribute, Session

from api.dependencies import GameFilters  
from api.schemas import FacetCount, FacetBundle  
from database.db import get_db  
from database.models import Game

router = APIRouter(tags=["facets"])

DbSession = Annotated[Session, Depends(get_db)]


def facet_query(  
    db: Session,  
    column: InstrumentedAttribute,  
    conditions: list,  
    q: Optional[str] = None,  
    sort: str = "count",  
    limit: Optional[int] = None,  
) -> List[FacetCount]:  
    """Distinct values of `column` with counts, honouring the active filters."""  
    stmt = (  
        select(column.label("value"), func.count().label("count"))  
        .where(column.is_not(None), column != "", *conditions)  
        .group_by(column)  
    )

    if q:  
        stmt = stmt.where(column.ilike(f"%{q}%"))

    if sort == "value":  
        stmt = stmt.order_by(column.asc())  
    else:  
        stmt = stmt.order_by(func.count().desc(), column.asc())

    if limit:  
        stmt = stmt.limit(limit)

    return [FacetCount(value=v, count=n) for v, n in db.execute(stmt).all()]  