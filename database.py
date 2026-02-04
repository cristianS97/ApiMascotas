import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', 'postgres')
host = os.getenv('DB_HOST', 'localhost') 
port = os.getenv('DB_PORT', 5433)
database = os.getenv('DB_NAME', 'veterinaria')
SQL_ALCHEMY_BATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(SQL_ALCHEMY_BATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
