from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

# Define the base class for all models
Base = declarative_base()

class BaseModel:

    """
    Base class for all database models, 
    providing common attributes and methods
    """

    # Primary key column
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        """
        Initialize a new model instance
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        """
        Human readable representation of the model instance
        """
        return "<{} {}>".format(self.__class__.__name__, self.id)
    
    def save(self):
        """
        Save the model instance to the database
        """

        from models import storage
        storage.new(self)
        storage.save()
    
    def delete(self):
        """
        Delete the model instance from the database
        """
        from models import storage
        storage.delete(self)
        storage.save()
    
    def to_dict(self):
        """
        Return a dictionary representation of the model instance
        """
        new_dict = self.__dict__.copy()
        new_dict.pop('_sa_instance_state', None)
        return new_dict