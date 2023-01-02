from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import app.models as models
from app.database import SessionLocal, engine
import jwt
import datetime
from app.settings import get_settings, Settings
from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import AbstractIncomingMessage
import json
import bcrypt
from app.list import get_server_list
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def generate_token(userid: int, username: str):
    now = datetime.datetime.utcnow()
    payload = {
        "iss": "master-server",
        "exp": (now + datetime.timedelta(hours=24)).timestamp(),
        "user_id": userid,
        "user_name": username
    }
    settings = get_settings()
    key = settings.JWT_SECRET
    encoded = jwt.encode(payload, key, algorithm="HS256")
    return encoded


@app.post("/login")
def login(login_dto: LoginDTO, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.login == login_dto.login).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect data")
    if not bcrypt.checkpw(login_dto.password.encode("utf-8"), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect data")
    return {'access_token': generate_token(db_user.id, db_user.login)}


@app.post("/register")
def create_user(register_dto: RegisterDTO, db: Session = Depends(get_db)):
    if register_dto.password != register_dto.pass_comp:
        raise HTTPException(status_code=400, detail="Incorrect data")
    hashed_password = bcrypt.hashpw(register_dto.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(login=register_dto.login, password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'id': db_user.id, 'login': db_user.login}


@app.get("/servers")
def read_servers(settings: Settings = Depends(get_settings), server_list: dict = Depends(get_server_list)):
    current_time = datetime.datetime.utcnow()
    filtered_list = list(filter(
        lambda item: item[1] + datetime.timedelta(seconds=settings.HEARTBEAT_RESPONSE_TIME) > current_time,
        server_list.items()
    ))
    mapped_list = list(map(lambda item: { 'address': f"{item[0][0]}:{item[0][1]}", 'last_heartbeat': item[1] }, filtered_list))
    return mapped_list


def upsert_server(address: str, port: int, server_list: dict = get_server_list()):
    server_list[(address, port)] = datetime.datetime.utcnow()


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        initial_server_data = message.body.decode("utf-8")
        server_data = json.loads(initial_server_data)
        upsert_server(server_data["advertised_address"], server_data["advertised_port"])


async def start_heartbeat_consume():
    settings = get_settings()
    connection = await connect_robust(settings.BROKER_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    heartbeat_exchange = await channel.declare_exchange(
        settings.HEARTBEAT_EXCHANGE_NAME, ExchangeType.FANOUT,
    )

    queue = await channel.declare_queue(exclusive=True)

    await queue.bind(heartbeat_exchange)

    await queue.consume(on_message)

    app.mq_connection = connection
    app.mq_channel = channel
    app.mq_heartbeat_exchange = heartbeat_exchange
    app.mq_heartbeat_queue = queue


app.add_event_handler("startup", start_heartbeat_consume)
