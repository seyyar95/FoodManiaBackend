from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import storage

class Ingredient(BaseModel, Base):
    """
    Ingredient model class, represents an ingredient
    """
    __tablename__ = 'ingredients'
    name = Column(String(128), nullable=False)
    img = Column(String(1024), nullable=True)

    # Define the many-to-many relationship between ingredients and foods
    foods = relationship("FoodIngredient", back_populates="ingredient")

