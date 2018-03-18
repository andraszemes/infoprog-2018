from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select

# ****** DB_INIT

# ESTABLISH DATABASE CONNECTION
dialect = 'sqlite:///database.db/'

# Create Database
engine = create_engine(dialect, encoding='utf8')

# Open session
session = Session(engine)

# Returns a new base class from which all mapped classes should inherit
Base = declarative_base()

# Container object that keeps together many different features of a database 
# (or multiple databases) being described
metadata = MetaData()
