from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class FoodSave(BaseModel, Base):
    __tablename__ = 'foods_save'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food_id = Column(Integer, ForeignKey('foods.id'), nullable=False)
    user = relationship("User", back_populates="usersave")
    food = relationship("Food", back_populates="foodsave")