from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import app.models as models
from app.database import SessionLocal, engine
import jwt
import datetime
from app.settings import get_settings
from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import AbstractIncomingMessage
import json
import bcrypt


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

server_list = dict()


class LoginDTO(BaseModel):
    login: str
    password: str


class RegisterDTO(BaseModel):
    login: str
    password: str
    pass_comp: str


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
    encoded=jwt.encode(payload, key, algorithm="HS256")
    return encoded


@app.post("/login")
def login(LoginDTO: LoginDTO, db: Session = Depends(get_db)):
    DB_user = db.query(models.User).filter(models.User.login == LoginDTO.login).first()
    if(DB_user is None):
        raise HTTPException(status_code=400, detail="Incorrect data")
    if not bcrypt.checkpw(LoginDTO.password.encode("utf-8"),DB_user.password):
        raise HTTPException(status_code=400, detail="Incorrect data")
    # if(LoginDTO.password != DB_user.password):
    #     raise HTTPException(status_code=400, detail="Incorrect data")
    return generate_token(DB_user.id, DB_user.login)


@app.post("/register/")
def create_user(RegisterDTO: RegisterDTO, db: Session = Depends(get_db)):
    if(RegisterDTO.password != RegisterDTO.pass_comp):
        raise HTTPException(status_code=400, detail="Incorrect data")
    hashed_password = bcrypt.hashpw(RegisterDTO.password.encode("utf-8"),bcrypt.gensalt())
    db_user = models.User(login=RegisterDTO.login, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/servers/")
def read_servers():
    current_time = datetime.datetime.utcnow()
    filtered_list = filter(lambda item: item[1]+datetime.timedelta(seconds=10)>current_time,server_list.items())
    filtered_list = dict(map(lambda item: (f"{item[0][0]}:{item[0][1]}", item[1]), filtered_list))
    return filtered_list


def upsert_server(Address: str, Port: int): 
    server_list[(Address,Port)] = datetime.datetime.utcnow()


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        initial_server_data = message.body.decode("utf-8")
        server_data = json.loads(initial_server_data)
        upsert_server(server_data["advertised_address"], server_data["advertised_port"])


async def start_heartbeat_consume():
    settings = get_settings()
    connection = await connect_robust(settings.BROKER_URL)
    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    heartbeat_exchange = await channel.declare_exchange(
        settings.HEARTBEAT_EXCHANGE_NAME, ExchangeType.FANOUT,
    )

    queue = await channel.declare_queue(exclusive=True)

    await queue.bind(heartbeat_exchange)

    await queue.consume(on_message)


app.add_event_handler("startup", start_heartbeat_consume)