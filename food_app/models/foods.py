from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text, func, select
from sqlalchemy.orm import relationship
from models import storage
from models.food_ingredient import FoodIngredient
from models.ingredients import Ingredient


class Food(BaseModel, Base):
    """
    Food model class, represents a food item
    """
    __tablename__ = 'foods'
    name = Column(String(128), nullable=False, unique=True)
    steps = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    time = Column(String(60), nullable=False)
    degree = Column(String(60), nullable=False)
    img = Column(String(1044), nullable=True)

    # Define the many-to-many relationship between foods and ingredients
    ingredients = relationship("FoodIngredient", back_populates="food")
    foodsave = relationship("FoodSave", back_populates="food")
    suggestion = relationship("DailySuggestion", back_populates="food")

    @classmethod
    def get_foods_by_ingredients(cls, ingredients):
        """
        Class method to get foods by ingredients
        """
        ingredient_ids = []

        for ing in ingredients:
            obj = storage.get_by_name(Ingredient, ing)
            if obj:
                ingredient_ids.append(obj.id)
            else:
                ingredient_ids.append(0)

        # Get the database session
        session = storage.get_session()

        # Query the database for foods that contain all the ingredients
        foods = session.query(cls) \
            .join(FoodIngredient) \
            .filter(FoodIngredient.ingredient_id.in_(ingredient_ids)) \
            .group_by(Food.id) \
            .having(func.count(FoodIngredient.id) == len(ingredient_ids))

        
        return foods