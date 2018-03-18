from dbinit import *
from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey, Text, String, Date, Enum, ForeignKeyConstraint
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base


# DEFINE SQLALCHEMY RELATIONSHIP MODELS
# Reader model
class Reader(Base):
    __tablename__ = 'readers'

    __table_args__ = (
            Column('id', Integer, primary_key=True),
            Column('code', String(10), unique=True),
            Column('name', Text),
            { 'mysql_collate': 'utf8_general_ci' }
        )
  
# Book Model
class Book(Base):
    __tablename__ = 'books'

    __table_args__ = (
            Column('id', Integer, primary_key=True),
            Column('code', String(10), unique=True),
            Column('title', Text),
            Column('value', Integer),
            Column('author', Text),
            Column('publisher', Text),
            Column('isbn', Text),
            Column('category', Text),
            { 'mysql_collate': 'utf8_general_ci' }
        )

# Magatine Model
class Magazine(Base):
    __tablename__ = 'magazines'

    __table_args__ = (
            Column('id', Integer, primary_key=True),
            Column('code', String(10), unique=True),
            Column('title', Text),
            Column('value', Integer),
            Column('publisher', Text),
            Column('issue', Integer),
            Column('volume', Integer),
            { 'mysql_collate': 'utf8_general_ci' }
        )

# Medium Model
class Medium(Base):
    __tablename__ = 'media'

    __table_args__ = (
            Column('id', Integer, primary_key=True),
            Column('code', String(10), unique=True),
            Column('type', Enum('CD', 'DVD', 'DIA')),
            Column('title', Text),
            Column('value', Integer),
            Column('release', Integer),
            Column('length', Integer),
            Column('color', String(2)),
            { 'mysql_collate': 'utf8_general_ci' }
        )

# Borrow Model
class Borrow(Base):
    __tablename__ = 'borrows'

    __table_args__ = (
            Column('id', Integer, primary_key=True),
            Column('reader_id', Integer, ForeignKey('readers.id')),
            Column('book_id', Integer, ForeignKey('books.id')),
            Column('magazine_id', Integer, ForeignKey('magazines.id')),
            Column('medium_id', Integer, ForeignKey('media.id')),
            Column('deadline', Date, server_default=datetime.now().date().strftime('%Y-%m-%d')),
            Column('extended', Integer, server_default='0')
        )

    readers = relationship(Reader)
    books = relationship(Book)
    media = relationship(Medium)
    magazines = relationship(Magazine)
    

Base.metadata.create_all(engine)