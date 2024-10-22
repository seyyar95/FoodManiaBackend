from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class FoodIngredient(BaseModel, Base):
    """
    FoodIngredient model class, represents the relationship between foods and ingredients
    """

    __tablename__ = "food_ingredient"
    food_id = Column(Integer, ForeignKey('foods.id'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    quantity = Column(String(60), nullable=False)

    
    # Define the many-to-many relationship between foods and ingredients
    food = relationship("Food", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="foods")