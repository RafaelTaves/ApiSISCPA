from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
import models, schemas, crud, auth, config
from dependencies import get_db, get_current_user
from database import engine
from auth import verify_token
from fastapi.middleware.cors import CORSMiddleware
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [ #No fim, alterar origins para somente o ip que irá fazer a requisição
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#------
#USER ENDPOINTS
#------

@app.post("/register", response_model=schemas.UsersRead, tags=["Authentication"])
def register(user: schemas.UsersCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    db_user = crud.get_user(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token, tags=["Authentication"])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/verify-token/{token}", tags=["Authentication"])
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}

@app.get("/me", response_model=schemas.UsersRead, tags=["Authentication"])
def read_users_me(current_user: schemas.UsersRead = Depends(get_current_user)):
    return current_user

#------
#CLIENT ENDPOINTS
#------

@app.post("/register_client", response_model=schemas.ClientRead, tags=["Client"])
def register_client(client: schemas.ClientCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    
    db_client = crud.get_client(db, cpf=client.cpf)
    if db_client:
        raise HTTPException(status_code=400, detail="Client already registered")
    
    return crud.create_client(db=db, client=client)


@app.get("/client/{cpf}", response_model=schemas.ClientRead, tags=["Client"])
def read_client(cpf: str, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):

    client = crud.get_client(db, cpf=cpf)

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return client

@app.patch("/client/{client_id}", response_model=schemas.ClientRead, tags=["Client"])
def update_client(client_id: int, client_update: schemas.ClientUpdate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    
    db_client = crud.get_client_by_id(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    updated_client = crud.update_client(db, db_client, client_update)
    
    return updated_client

@app.delete("/client/{client_id}", response_model=schemas.ClientRead, tags=["Client"])
def delete_client(client_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    
    return crud.delete_client(db, client_id)

#------
# SUBSCRIPTIONS ENDPOINTS
#------

@app.post("/subscriptions", response_model=schemas.SubscriptionRead, tags=["Subscription"])
def register_subscription(subscription: schemas.SubscriptionCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    
    client = crud.get_client_by_id(db, subscription.id_client)
    if not client:
        raise HTTPException(status_code=400, detail="Client not found. Cannot create subscription.")

    return crud.create_subscription(db=db, subscription=subscription)


@app.get("/subscription/{subscription_id}", response_model=List[schemas.SubscriptionRead], tags=["Subscription"])
def read_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):

    subscription = crud.get_subscription_by_id(db, subscription_id)

    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")

    return subscription

@app.get("/subscriptions/client/{client_id}", response_model=List[schemas.SubscriptionRead], tags=["Subscription"])
def read_subscriptions_by_client(client_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    subscriptions = db.query(models.Subscriptions).filter(models.Subscriptions.id_client == client_id).all()
    
    if not subscriptions:
        raise HTTPException(status_code=404, detail="Nenhuma assinatura encontrada para este cliente.")

    return [schemas.SubscriptionRead.model_validate(sub) for sub in subscriptions]  # 🔹 Converte para schema correto

@app.patch("/subscription/{subscription_id}", response_model=schemas.SubscriptionRead, tags=["Subscription"])
def update_subscription(subscription_id: int, subscription_update: schemas.SubscriptionCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    
    db_subscription = crud.get_subscription_by_id(db, subscription_id)
    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    updated_subscription = crud.update_subscription(db, db_subscription, subscription_update)
    
    return updated_subscription

@app.delete("/subscriptions/{subscription_id}", response_model=schemas.SubscriptionRead, tags=["Subscription"])
def delete_subscription(subscription_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):

    return crud.delete_subscription(db, subscription_id)

#------
# ADRESS ENDPOINTS
#------

@app.post("/adress", response_model=schemas.AdressRead, tags=["Adress"])
def create_adress_endpoint(adress: schemas.AdressCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    return crud.create_adress(db, adress)

@app.get("/adress/{adress_id}", response_model=schemas.AdressRead, tags=["Adress"])
def get_adress_endpoint(adress_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    adress = crud.get_adress(db, adress_id)
    if not adress:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return adress

@app.get("/adress/", response_model=List[schemas.AdressRead], tags=["Adress"])
def get_all_adresses_endpoint(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    adresses = crud.get_all_adresses(db)
    return [schemas.AdressRead.model_validate(a) for a in adresses]

@app.get("/adress/client/{client_id}", response_model=List[schemas.AdressRead], tags=["Adress"])
def get_adresses_by_client_endpoint(client_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    adresses = crud.get_adresses_by_client(db, client_id)
    if not adresses:
        raise HTTPException(status_code=404, detail="Nenhum endereço encontrado para este cliente")
    return [schemas.AdressRead.model_validate(a) for a in adresses]

@app.patch("/adress/{adress_id}", response_model=schemas.AdressRead, tags=["Adress"])
def update_adress_endpoint(adress_id: int, adress_update: schemas.AdressCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    updated_adress = crud.update_adress(db, adress_id, adress_update)
    if not updated_adress:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return updated_adress

@app.delete("/adress/{adress_id}", tags=["Adress"])
def delete_adress_endpoint(adress_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    if not crud.delete_adress(db, adress_id):
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return {"message": "Endereço deletado com sucesso"}

#------
# BARBER ENDPOINTS
#------

@app.post("/barber/", response_model=schemas.BarberRead, tags=["Barber"])
def create_barber_endpoint(barber: schemas.BarberCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    return crud.create_barber(db, barber)

@app.get("/barber/{barber_id}", response_model=schemas.BarberRead, tags=["Barber"])
def get_barber_endpoint(barber_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    barber = crud.get_barber(db, barber_id)
    if not barber:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado")
    return barber

@app.get("/barber/", response_model=List[schemas.BarberRead], tags=["Barber"])
def get_all_barbers_endpoint(db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    barbers = crud.get_all_barbers(db)
    return [schemas.BarberRead.model_validate(b) for b in barbers]

@app.patch("/barber/{barber_id}", response_model=schemas.BarberRead, tags=["Barber"])
def update_barber_endpoint(barber_id: int, barber_update: schemas.BarberCreate, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    updated_barber = crud.update_barber(db, barber_id, barber_update)
    if not updated_barber:
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado")
    return updated_barber


@app.delete("/barber/{barber_id}", tags=["Barber"])
def delete_barber_endpoint(barber_id: int, db: Session = Depends(get_db), current_user: schemas.UsersRead = Depends(get_current_user)):
    if not crud.delete_barber(db, barber_id):
        raise HTTPException(status_code=404, detail="Barbeiro não encontrado")
    return {"message": "Barbeiro deletado com sucesso"}
