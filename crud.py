from sqlalchemy.orm import Session
import models, schemas
from auth import get_password_hash
from fastapi import HTTPException

def get_user(db: Session, login: str):
    return db.query(models.Users).filter(models.Users.login == login).first()

def create_user(db: Session, user: schemas.UsersCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.Users(login=user.login, hashed_password=hashed_password, position=user.position)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#------
#CLIENT CRUD
#------

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Clients(cpf=client.cpf, name=client.name, phone=client.phone)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client(db:Session, cpf: str):
    return db.query(models.Clients).filter(models.Clients.cpf == cpf).first()

def get_client_by_name(db:Session, name: str):
    return db.query(models.Clients).filter(models.Clients.name == name).first()

def get_client_by_id(db: Session, client_id: int):
    return db.query(models.Clients).filter(models.Clients.id_client == client_id).first()


def update_client(db: Session, db_client: models.Clients, client_update: schemas.ClientUpdate):
    for key, value in client_update.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = db.query(models.Clients).filter(models.Clients.id_client == client_id).first()

    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(db_client)
    db.commit()

    return db_client

#------
#SUBSCRIPTION CRUD
#------

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    db_subscription = models.Subscriptions(
        start_date=subscription.start_date,
        duration=subscription.duration,
        payment_method=subscription.payment_method,
        end_date=subscription.end_date,
        id_client=subscription.id_client
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_subscription_by_id(db: Session, subscription_id: int):
    return db.query(models.Subscriptions).filter(models.Subscriptions.id_subscription == subscription_id).first()

def get_subscriptions_by_client(db: Session, client_id: int):
    return db.query(models.Subscriptions).filter(models.Subscriptions.id_client == client_id).all()

def update_subscription(db: Session, db_subscription: models.Subscriptions, subscription_update: schemas.SubscriptionCreate):
    for key, value in subscription_update.dict(exclude_unset=True).items():
        setattr(db_subscription, key, value)
    
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def delete_subscription(db: Session, subscription_id: int):
    db_subscription = db.query(models.Subscriptions).filter(models.Subscriptions.id_subscription == subscription_id).first()

    if not db_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(db_subscription)
    db.commit()

    return db_subscription

#------
#ADRESS CRUD
#------

def create_adress(db: Session, adress: schemas.AdressCreate):
    db_adress = models.Adress(**adress.model_dump())
    db.add(db_adress)
    db.commit()
    db.refresh(db_adress)
    return db_adress

def get_adress(db: Session, adress_id: int):
    return db.query(models.Adress).filter(models.Adress.id_adress == adress_id).first()

def get_adresses_by_client(db: Session, client_id: int):
    return db.query(models.Adress).filter(models.Adress.id_client == client_id).all()

def get_all_adresses(db: Session):
    return db.query(models.Adress).all()

def update_adress(db: Session, adress_id: int, adress_update: schemas.AdressCreate):
    db_adress = db.query(models.Adress).filter(models.Adress.id_adress == adress_id).first()
    if not db_adress:
        return None
    
    for key, value in adress_update.model_dump().items():
        setattr(db_adress, key, value)
    
    db.commit()
    db.refresh(db_adress)
    return db_adress


def delete_adress(db: Session, adress_id: int):
    db_adress = db.query(models.Adress).filter(models.Adress.id_adress == adress_id).first()
    if db_adress:
        db.delete(db_adress)
        db.commit()
        return True
    return False

#------
#BARBER CRUD
#------

def create_barber(db: Session, barber: schemas.BarberCreate):
    db_barber = models.Barber(**barber.model_dump())
    db.add(db_barber)
    db.commit()
    db.refresh(db_barber)
    return db_barber

def get_barber(db: Session, barber_id: int):
    return db.query(models.Barber).filter(models.Barber.id_barber == barber_id).first()

def get_all_barbers(db: Session):
    return db.query(models.Barber).all()

def update_barber(db: Session, barber_id: int, barber_update: schemas.BarberCreate):
    db_barber = db.query(models.Barber).filter(models.Barber.id_barber == barber_id).first()
    if not db_barber:
        return None
    
    for key, value in barber_update.model_dump().items():
        setattr(db_barber, key, value)
    
    db.commit()
    db.refresh(db_barber)
    return db_barber

def delete_barber(db: Session, barber_id: int):
    db_barber = db.query(models.Barber).filter(models.Barber.id_barber == barber_id).first()
    if db_barber:
        db.delete(db_barber)
        db.commit()
        return True
    return False
