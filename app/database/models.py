from datetime import datetime
from sqlalchemy import BigInteger, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import enum

class Base(DeclarativeBase):
    pass

class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    PURCHASE = "purchase"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class UserbotSession(Base):
    __tablename__ = "userbot_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    phone_number: Mapped[str] = mapped_column(String(20))
    session_string: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    amount: Mapped[float] = mapped_column(Float)
    tx_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
