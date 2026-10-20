from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, Transaction, TransactionType

async def get_or_create_user(session: AsyncSession, user_id: int, full_name: str, username: str) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(id=user_id, full_name=full_name, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user

async def get_user_balance(session: AsyncSession, user_id: int) -> float:
    stmt = select(User.balance).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() or 0.0

async def update_balance(session: AsyncSession, user_id: int, amount: float, tx_type: TransactionType, description: str = None) -> None:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user:
        if tx_type == TransactionType.DEPOSIT:
            user.balance += amount
        elif tx_type == TransactionType.PURCHASE:
            user.balance -= amount
            
        tx = Transaction(user_id=user_id, amount=amount, tx_type=tx_type, description=description)
        session.add(tx)
        await session.commit()