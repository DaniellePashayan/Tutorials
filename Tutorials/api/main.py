from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from models import VideoGames

app = FastAPI()

connection_string = "sqlite:///lego_sets.db"
engine = create_engine(connection_string)

