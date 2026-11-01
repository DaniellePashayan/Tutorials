from sqlalchemy import create_engine, Integer, String, Float, Column
from sqlalchemy.orm import DeclarativeBase, Session

CONN_STRING = 'sqlite:///video_games_data.db'

class Base():
    pass

class VideoGames():
    __tablename__ = "video_games"
    
    # add column schema below. you will need to review the data and see what column(s) can be used as primary key(s)

    def __repr__(self):
        # should print title, console, release date, genre, and critic score
        return