#With an ORM, you normally create a class that represents a table in a SQL database, each attribute of the class represents a column, with a name and a type.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@postgresserver/nortwind.sql"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base()

