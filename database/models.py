from sqlalchemy import Boolean, Integer, String, Float, Column, MetaData, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()

class Base(DeclarativeBase):
    pass

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    img = Column(String, nullable=True)
    title = Column(String, nullable=True, index=True)
    console = Column(String, nullable=True, index=True)
    genre = Column(String, nullable=True, index=True)
    publisher = Column(String, nullable=True, index=True)
    developer = Column(String, nullable=True, index=True)
    critic_score = Column(Float, nullable=True)
    total_sales = Column(Float, nullable=True, index=True)
    na_sales = Column(Float, nullable=True)
    jp_sales = Column(Float, nullable=True)
    pal_sales = Column(Float, nullable=True)
    other_sales = Column(Float, nullable=True)
    release_date = Column(String, nullable=True)
    last_update = Column(String, nullable=True)
    
    __table_args__ = (  
        Index("ix_games_console_genre", "console", "genre"),  
    ) 

    def __repr__(self):
        return f"<VideoGame(name={self.title}, console={self.console}, release_date={self.release_date}, genre={self.genre}, rating={self.critic_score})>"
    
class User(Base):  
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  
    username: Mapped[str] = mapped_column(String, unique=True, index=True)  
    hashed_password: Mapped[str] = mapped_column(String)  
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)  
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)  