from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text, func, select
from sqlalchemy.orm import relationship
from models import storage
from models.food_ingredient import FoodIngredient
from models.ingredients import Ingredient


class DailySuggestion(BaseModel, Base):
    __tablename__ = 'daily_suggestion'
    food_id = Column(Integer, ForeignKey('foods.id'), nullable=False)

    food = relationship("Food", back_populates="suggestion")

    