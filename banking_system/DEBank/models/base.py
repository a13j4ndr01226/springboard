
from sqlalchemy import create_engine
"""
-ORM = Object Related Mapper
-declarative_base creates base class that all models will inherit
-sessionmaker creates a session to talk to the DB, Run queries, Insert, Update, and delete records
"""
from sqlalchemy.orm import declarative_base, sessionmaker 

import os 

#Creates 'db' folder if it doesn't already exist
os.makedirs("db", exist_ok=True) 

engine = create_engine("sqlite:///db/bank.db", echo=True) #echo=True tells SQLAlchemy to print every SQL command it runs

"""
Sets a temporary workspace to query data, add new records, commit changes. 
autoflush=False prevents SQLAlchemy from sending changes before you explicitly commit
"""
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()





