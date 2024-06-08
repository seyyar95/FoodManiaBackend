from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import storage

class Ingredient(BaseModel, Base):
    __tablename__ = 'ingredients'
    name = Column(String(128), nullable=False)

    foods = relationship("FoodIngredient", back_populates="ingredient")

    @classmethod
    def get_ingredients_ids(cls, ingredients):
        session = storage.get_session()
        ingredients_ids = []
        for ingredient in ingredients:
            ingredient = session.query(cls).filter_by(name=ingredient).first()
            if ingredient:
                ingredients_ids.append({
                    'name': ingredient.name,
                    'id': ingredient.id}
                    )
        return ingredients_ids

