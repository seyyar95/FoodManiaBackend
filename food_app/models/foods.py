from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text, func, select
from sqlalchemy.orm import relationship
from models import storage
from models.food_ingredient import FoodIngredient
from models.ingredients import Ingredient


class Food(BaseModel, Base):
    __tablename__ = 'foods'
    name = Column(String(128), nullable=False, unique=True)
    recipe = Column(Text, nullable=False)
    img = Column(String(128), nullable=True)

    ingredients = relationship("FoodIngredient", back_populates="food")
    foodsave = relationship("FoodSave", back_populates="food")

    @classmethod
    def get_foods_by_ingredients(cls, ingredients):
        ingredient_ids = []

        for ing in ingredients:
            obj = storage.get_by_name(Ingredient, ing)
            if obj:
                ingredient_ids.append(obj.id)
            else:
                ingredient_ids.append(0)

        session = storage.get_session()
        foods = session.query(cls) \
            .join(FoodIngredient) \
            .filter(FoodIngredient.ingredient_id.in_(ingredient_ids)) \
            .group_by(Food.id) \
            .having(func.count(FoodIngredient.id) == len(ingredient_ids))

        
        return foods