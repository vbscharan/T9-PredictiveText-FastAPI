from application.models.DatabaseConfiguration import *
from psycopg2.extras import RealDictCursor
from threading import *

class SingletonDatabaseConnection:
    _instance = None
    _lock=Lock()
    @staticmethod
    def getInstance():
        if SingletonDatabaseConnection._instance is None:
            with SingletonDatabaseConnection._lock:
                if SingletonDatabaseConnection._instance is None:
                    SingletonDatabaseConnection._instance=SingletonDatabaseConnection()
                    
                    SingletonDatabaseConnection._instance.db=Database("localhost", "contactsbook", "postgres", "vBhanu", RealDictCursor)
                    if SingletonDatabaseConnection._instance.db.error is not None:
                        print(SingletonDatabaseConnection._instance.db.error)
                        raise Exception(SingletonDatabaseConnection._instance.db.error)
        return SingletonDatabaseConnection._instance
    
    '''
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.db = Database("localhost", "contactsbook", "postgres", "vBhanu", RealDictCursor)
            if cls._instance.db.error is not None:
                print(cls._instance.db.error)
                raise Exception(cls._instance.db.error)
        return cls._instance
    '''
