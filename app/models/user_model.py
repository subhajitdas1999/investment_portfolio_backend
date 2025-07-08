from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
# Base is imported from the top-level app.__init__
from app.__init__ import Base

class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"