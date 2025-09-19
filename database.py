from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "add your mysql database url"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
