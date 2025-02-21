from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URL
from dotenv import load_dotenv
import os

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"options": "-c client_encoding=UTF8"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

