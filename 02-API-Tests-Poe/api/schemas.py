from datetime import date, datetime  
from typing import Optional, List  
from pydantic import BaseModel, ConfigDict, Field

class GameOut(BaseModel):  
    model_config = ConfigDict(from_attributes=True)  # read from ORM objects

    id: int  
    img: Optional[str] = None  
    title: str  
    console: str  
    genre: Optional[str] = None  
    publisher: Optional[str] = None  
    developer: Optional[str] = None  
    critic_score: Optional[float] = Field(None, description="0-10 scale")  
    total_sales: Optional[float] = Field(None, description="Millions of units")  
    na_sales: Optional[float] = Field(None, description="Millions of units")  
    jp_sales: Optional[float] = Field(None, description="Millions of units")  
    pal_sales: Optional[float] = Field(None, description="Millions of units")  
    other_sales: Optional[float] = Field(None, description="Millions of units")  
    release_date: Optional[date] = None  
    last_update: Optional[date] = None

class GamePage(BaseModel):  
    items: List[GameOut]  
    total: int  
    limit: int  
    offset: int

class GenreStats(BaseModel):  
    genre: Optional[str]  
    game_count: int  
    total_sales: Optional[float]  
    avg_critic_score: Optional[float]
    
class FacetCount(BaseModel):  
    value: str  
    count: int

class FacetBundle(BaseModel):  
    consoles: List[FacetCount]  
    genres: List[FacetCount]  
    publishers: List[FacetCount]  
    developers: List[FacetCount]  
    total_games: int  

class Token(BaseModel):  
    access_token: str  
    token_type: str = "bearer"
    expires_in: int
    expires_at: datetime


class UserRead(BaseModel):  
    model_config = ConfigDict(from_attributes=True)

    id: int  
    username: str  
    full_name: str | None = None  
    disabled: bool 
    is_admin: bool = False