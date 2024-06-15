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
    img = Column(String(128), nullable=True)

    # Define the many-to-many relationship between ingredients and foods
    foods = relationship("FoodIngredient", back_populates="ingredient")

    @classmethod
    def get_ingredients_ids(cls, ingredients):
        """
        Class method to get ingredient ids
        """

        # Get the database session
        session = storage.get_session()

        ingredients_ids = []
        for ingredient in ingredients:
            # Query the database for the ingredient
            ingredient = session.query(cls).filter_by(name=ingredient).first()
            if ingredient:
                ingredients_ids.append({
                    'name': ingredient.name,
                    'id': ingredient.id}
                    )
        return ingredients_ids

