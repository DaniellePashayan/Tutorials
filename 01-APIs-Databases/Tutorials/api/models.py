from sqlalchemy import Integer, String, Float, Column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class LegoSet(Base):
    __tablename__ = 'lego_sets'
    
    set_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    theme = Column(String, nullable=False)
    subtheme = Column(String, nullable=True)
    themeGroup = Column(String, nullable=True)
    category = Column(String, nullable=True)
    pieces = Column(Integer, nullable=True)
    minifigs = Column(Integer, nullable=True)
    agerange_min = Column(Integer, nullable=True)
    US_retailPrice = Column(Float, nullable=True)
    bricksetURL = Column(String, nullable=True)
    thumbnailURL = Column(String, nullable=True)
    imageURL = Column(String, nullable=True)