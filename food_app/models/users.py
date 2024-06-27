from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from models import storage


class User(BaseModel, Base):
    """
    User model class, represents a user in the application
    """
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)

    # Define the many-to-many relationship between users and foods
    usersave = relationship("FoodSave", back_populates="user")

    
    def set_password(self, password):
        # Generate a password hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # Check if the password is correct
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_user_by_email(cls, email):
        """
        Class method to get a user by email
        """
        session = storage.get_session()
        
        # Query the database for the user by email
        user = session.query(cls).filter_by(email=email).first()
        return user
