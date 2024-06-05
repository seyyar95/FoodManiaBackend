from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format('food_mania',
                                             'food_mania_pwd',
                                             'localhost',
                                             'food_mania_db'), pool_pre_ping=True)


    
    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)
    
    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()
    
    def delete(self, obj=None):
        """Delete obj from the current database session if not None."""
        if obj is not None:
            self.__session.delete(obj)
        
    def all(self, cls=None):
        dictionary = {}

        
        for instance in self.__session.query(cls).all():
            key = f"{cls.__name__}.{instance.id}"
            dictionary[key] = instance
        return dictionary
    
    def reload(self):
        """Create all tables in the database and initialize a session."""
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
    
    def close(self):
        """Close the current session."""
        self.__session.remove()