from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)



class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    name = Column(String)
    updated_at = Column(DateTime)
