from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # project root  
DATABASE_URL = f"sqlite:///{BASE_DIR / 'video_games_data.db'}"  

engine = create_engine(  
    DATABASE_URL,  
    # SQLite-only: FastAPI may touch the connection from different  
    # threads. Safe here because each request gets its own session.  
    connect_args={"check_same_thread": False},  
    echo=False,  # flip to True to watch the generated SQL  
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db():  
    db = SessionLocal()  
    try:  
        yield db  
    finally:  
        db.close() 