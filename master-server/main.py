from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import crud, models, schemas
from .database import SessionLocal, engine

import pika
import jwt
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from pydantic import BaseSettings
from functools import lru_cache
from .settings import get_settings

import asyncio

from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage
from ast import literal_eval
from dependency_injector.wiring import Provide, inject


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class LoginDTO(BaseModel):
    login: str
    password: str

class RegisterDTO(BaseModel):
    login: str
    password: str
    pass_comp: str




# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def generate_token(userid:int, username:str):
    now = datetime.datetime.utcnow()
    payload = {
        "iss":"master-server",
        "exp":(now+datetime.timedelta(hours=24)).timestamp(),
        "user_id": userid,
        "user_name": username

    }
    settings = get_settings()
    key = settings.JWT_SECRET
    encoded=jwt.encode({"some": payload}, key, algorithm="HS256")
    return encoded



@app.post("/login")
def login(LoginDTO: LoginDTO, db: Session = Depends(get_db)):
    DB_user = db.query(models.User).filter(models.User.login == LoginDTO.login).first()
    if(DB_user is None):
        raise HTTPException(status_code=400, detail="Incorrect data")
    
    if(LoginDTO.password != DB_user.password):
        raise HTTPException(status_code=400, detail="Incorrect data")
    return generate_token(DB_user.id, DB_user.login)


@app.post("/register/")
def create_user(RegisterDTO: RegisterDTO, db: Session = Depends(get_db)):
    if(RegisterDTO.password != RegisterDTO.pass_comp):
        raise HTTPException(status_code=400, detail="Incorrect data")
    db_user = models.User(login=RegisterDTO.login, password=RegisterDTO.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/servers/")
def read_servers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Server).offset(skip).limit(limit).all()


def upsert_server(Address: str, Port: int):
    db = SessionLocal()
    address = f"{Address}:{Port}"
    DB_server = db.query(models.Server).filter(models.Server.address == address).first()
    if( DB_server is None):
        new_server = models.Server(address=address, name=address, updated_at=datetime.datetime.utcnow())
        db.add(new_server)
        db.commit()
        db.refresh(new_server)    
    else:
        DB_server.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(DB_server)
    db.close()


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        initial_server_data = message.body.decode("utf-8")
        server_data = literal_eval(initial_server_data)
        upsert_server(server_data["advertised_address"], server_data["advertised_port"])
        


async def main() -> None:
    # Perform connection
    settings = get_settings()
    connection = await connect("amqp://user:password@localhost")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        heartbeat_exchange = await channel.declare_exchange(
            "heartbeat-exchange", ExchangeType.FANOUT,
        )

        # Declaring queue
        queue = await channel.declare_queue(exclusive=True)

        # Binding the queue to the exchange
        await queue.bind(heartbeat_exchange)

        # Start listening the queue
        await queue.consume(on_message)

        print(" [*] Waiting for logs. To exit press CTRL+C")
        await asyncio.Future()

async def f():
    asyncio.create_task(main())
app.add_event_handler("startup", f)


