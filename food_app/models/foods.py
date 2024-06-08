from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from models import storage
from models.food_ingredient import FoodIngredient
from models.ingredients import Ingredient


class Food(BaseModel, Base):
    __tablename__ = 'foods'
    name = Column(String(128), nullable=False, unique=True)
    recipe = Column(Text, nullable=False)

    ingredients = relationship("FoodIngredient", back_populates="food")

    @classmethod
    def get_foods_by_ingredients(cls, ingredient_ids):
        session = storage.get_session()
        
        foods = session.query(cls, FoodIngredient).join(FoodIngredient).join(Ingredient).filter(Ingredient.id.in_(ingredient_ids)).all()

        return foods