from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Food(BaseModel, Base):
    __tablename__ = 'foods'
    name = Column(String(128), nullable=False)
    recipe = Column(Text, nullable=False)
    ingredients = relationship('Ingredient', backref='food', cascade='all, delete')