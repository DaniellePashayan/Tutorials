from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.db import engine
from database.models import Base, Game


CSV_PATH = Path(__file__).resolve().parent / "video_games_data.csv"


def drop_and_create_db() -> None:
    Base.metadata.drop_all(engine)
    with engine.begin() as conn:
        conn.execute(text("DROP INDEX IF EXISTS ix_games_console_genre"))
        conn.execute(text("DROP TABLE IF EXISTS video_games"))
    Base.metadata.create_all(engine)


def populate_db() -> None:
    data = pd.read_csv(CSV_PATH)
    records = data.to_dict(orient="records")
    game_rows = [Game(**{str(k): v for k, v in row.items()}) for row in records]

    with Session(engine) as session:
        session.add_all(game_rows)
        session.commit()


def reset_db() -> None:
    drop_and_create_db()
    populate_db()


if __name__ == "__main__":
    reset_db()