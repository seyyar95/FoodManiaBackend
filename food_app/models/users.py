from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from models import storage


class User(BaseModel, Base):
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    profile_picture = Column(String(128), nullable=True)

    usersave = relationship("FoodSave", back_populates="user")

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_user_by_email(cls, email):
        session = storage.get_session()
        user = session.query(cls).filter_by(email=email).first()
        return user
