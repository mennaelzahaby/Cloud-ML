from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class ModelRegistry(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    version = Column(String)
    accuracy = Column(Float)
    path = Column(String)
    active = Column(Boolean, default=True)
