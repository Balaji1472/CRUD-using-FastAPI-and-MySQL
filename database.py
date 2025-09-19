from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "mysql+mysqlconnector://root:Balaji%4045@localhost:3306/product_tracker"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
