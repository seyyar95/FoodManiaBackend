from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Ingredient(BaseModel, Base):
    __tablename__ = 'ingredients'
    name = Column(String(128), nullable=False)