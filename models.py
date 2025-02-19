from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Users(Base):
    __tablename__ = "Users"
    id_user = Column(Integer, primary_key=True, index=True)
    login  = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(60))
    position = Column(String(45)) 
    
class Clients(Base):
    __tablename__ = "Clients"
    id_client = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(11))
    name = Column(String(60))
    phone = Column(String(12))

class Subscriptions(Base):
    __tablename__ = "Subscriptions"
    id_subscription = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    duration = Column(Integer)
    payment_method = Column(String(45))
    end_date = Column(Date) 
    id_client = Column(Integer, index=True)
    
class Adress(Base):
    __tablename__ = "Adress"
    id_adress = Column(Integer, primary_key=True, index=True)
    logradouro = Column(String(45))
    number = Column(String(45))
    neighborhood = Column(String(45))
    city = Column(String(45))
    complement = Column(String(45)) 
    id_client = Column(Integer, index=True)
    
class Barber(Base):
    __tablename__ = "Barber"
    id_barber = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    
# class users_clients(Base):
#     __tablename__ = "users_clients"
#     id_user = Column(Integer, ForeignKey("Users.id_user"), primary_key=True)
#     id_client = Column(Integer, ForeignKey("Clients.id_client"), primary_key=True)