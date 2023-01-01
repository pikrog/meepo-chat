import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum

from database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class MessageType(str, enum.Enum):
    chat = "chat"
    join = "join"
    leave = "leave"


class QueuedMessage:
    def __init__(
            self,
            type: str,
            timestamp: str,
            advertised_address: str,
            advertised_port: int,
            text: str | None = None,
            sender: str | None = None,
            sender_id: int | None = None,
    ):
        self.type = type
        self.timestamp = timestamp
        self.advertised_address = advertised_address
        self.advertised_port = advertised_port
        self.text = text
        self.sender = sender
        self.sender_id = sender_id


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    advertised_server = Column(String, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    type = Column(Enum(MessageType), nullable=False)
    text = Column(String)
    timestamp = Column(DateTime, nullable=False)


class InvalidMessage(Base):
    __tablename__ = "invalid_messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)


Base.metadata.create_all(engine)
