from db.database import get_session
from db.models import Payment
from sqlalchemy.future import select
from sqlalchemy import update
from config.subscribtion import SUBS


async def create_payment(user_id, telegram_id, subscription_type, invoice_id, email):
    sub_info = SUBS.get(subscription_type)
    async with get_session() as session:
        payment = Payment(
            user_id=user_id,
            telegram_id=telegram_id,
            subscription_type=subscription_type,
            invoice_id=invoice_id,
            email=email,
            amount = sub_info['amount'],
            description = sub_info['description'],
            currency = sub_info['currency']
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment


async def get_payment(invoice_id):
    async with get_session() as session:
        stmt = select(Payment).where(Payment.invoice_id == invoice_id)
        result = await session.execute(stmt)
        payment = result.scalars().first()
        return payment

async def update_payment(invoice_id, status):
    async with get_session() as session:
        stmt = update(Payment).where(Payment.invoice_id == invoice_id).values(status = status)
        await session.execute(stmt)
        await session.commit()
        return await get_payment(invoice_id)