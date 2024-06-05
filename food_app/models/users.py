from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib


class User(BaseModel, Base):
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password_hash = Column(String(256), nullable=False)
    profile_picture = Column(String(128), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def set_password(self, password):
    #     self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # def check_password(self, password):
    #     return self.password_hash == hashlib.sha256(password.encode()).hexdigest()