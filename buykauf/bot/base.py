
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

#engine = create_engine(
#    "sqlite://",
#    connect_args={"check_same_thread": False},
#    poolclass=StaticPool
#)

engine = create_engine('sqlite:///../db/buykauf.sqlite3')

Session = sessionmaker(bind=engine)

Base = declarative_base()




