from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class BaseModel:
    id = Column(String(60), nullable=False, primary_key=True)

    def __init__(self, *args, **kwargs):
        
        self.id = str(uuid.uuid4())
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return "<{} {}>".format(self.__class__.__name__, self.id)
    
    def save(self):
        from models import storage
        storage.new(self)
        storage.save()
    
    def delete(self):
        from models import storage
        storage.delete(self)
        storage.save()
    
    def to_dict(self):
        new_dict = self.__dict__.copy()
        new_dict.pop('_sa_instance_state', None)
        return new_dict