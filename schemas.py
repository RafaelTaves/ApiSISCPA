from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from typing import List

#Users schemas
class UsersBase(BaseModel):
    login: str 
    
class UsersCreate(UsersBase):
    password: str
    position: str
    
    class Config:
        from_attributes = True

class UsersRead(UsersBase):
    id_user: int

    class Config:
        from_attributes = True

#Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    
#Clients schemas
class ClientBase(BaseModel):
    cpf: str
    name: str
    phone: str

class ClientCreate(ClientBase):
    pass

    class Config:
        from_attributes = True

class ClientRead(ClientBase):
    id_client: int
    
    class Config:
        from_attributes = True

class ClientUpdate(BaseModel):
    cpf: str
    name: str
    phone: str
        
#Subscriptions schemas
class SubscriptionsBase(BaseModel):
    start_date: date
    duration: int
    payment_method: str
    end_date: date 
    id_client: int
    
    class Config:
        from_attributes = True
    
class SubscriptionCreate(SubscriptionsBase):
    pass

    class Config:
        from_attributes = True

class SubscriptionRead(SubscriptionsBase):
    id_subscription: int
    
    class Config:
        from_attributes = True
        
#Adress schemas
class AdressBase(BaseModel):
    logradouro: str
    number: str
    neighborhood: str
    city: str
    complement: str 
    id_client: int
    
class AdressCreate(AdressBase):
    pass

    class Config:
        from_attributes = True

class AdressRead(AdressBase):
    id_adress: int
    
    class Config:
        from_attributes = True

#Barber Schemas

class BarberBase(BaseModel):
    name: str  

class BarberCreate(BarberBase):
    pass

    class Config:
        from_attributes = True
    
class BarberRead(BarberBase):
    id_barber: int
    
    class Config:
        from_attributes = True

#users_clients associative schema

# class UsersClientBase(BaseModel):
#     id_user: int
#     id_client: int

# class UsersClientCreate(UsersClientBase):
#     pass

#     class Config:
#         from_attributes = True

# class UsersClientRead(UsersClientBase):
#     class Config:
#         from_attributes = True 