from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class FoodSave(BaseModel, Base):
    """
    FoodSave model class, represents the relationship between users and foods they save
    """
    __tablename__ = 'foods_save'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food_id = Column(Integer, ForeignKey('foods.id'), nullable=False)

    # Define the many-to-many relationship between users and foods
    user = relationship("User", back_populates="usersave")
    food = relationship("Food", back_populates="foodsave")