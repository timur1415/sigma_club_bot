from db.database import get_session
from db.models import User
from sqlalchemy.future import select
from sqlalchemy import update
from dateutil import relativedelta

from datetime import datetime, timedelta, UTC

from dateutil.relativedelta import relativedelta


async def create_user(telegram_id, username):
    async with get_session() as session:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user


async def get_user(telegram_id):
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        return user


async def add_email(telegram_id, email):
    async with get_session() as session:
        stmt = update(User).where(User.telegram_id == telegram_id).values(email=email)
        await session.execute(stmt)
        await session.commit()
        return await get_user(telegram_id)


async def update_user_substatus(telegram_id, sub_status, subscription_type):
    async with get_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        user.sub_status = sub_status
        if sub_status == "active":
            now = datetime.now(UTC)
            if subscription_type == "1_month_rf":
                user.sub_end_date = now + relativedelta(months=1)
                user.sub_ban_date = now + relativedelta(months=1, days=2)
            elif subscription_type == "3_month_rf":
                user.sub_end_date = now + relativedelta(months=3)
                user.sub_ban_date = now + relativedelta(months=3, days=2)
            elif subscription_type == "6_month_rf":
                user.sub_end_date = now + relativedelta(months=6)
                user.sub_ban_date = now + relativedelta(months=6, days=2)
            elif subscription_type == "12_month_rf":
                user.sub_end_date = now + relativedelta(months=12)
                user.sub_ban_date = now + relativedelta(months=1, days=2)
        await session.commit()
        return await get_user(telegram_id)
    
async def get_all_debtors():
    async with get_session() as session:
        stmt = select(User).where(User.sub_ban_date < datetime.now(UTC), User.sub_status == 'active')
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users
    
async def update_all_debtors():
    async with get_session() as session:
        stmt = update(User).where(User.sub_ban_date < datetime.now(UTC), User.sub_status == 'active').values(sub_status='expired')
        await session.execute(stmt)
        await session.commit()
