from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, func, ForeignKey, Text
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    sub_end_date = Column(DateTime, nullable=True)
    sub_ban_date = Column(DateTime, nullable=True)
    sub_status = Column(String, default='inactive')  # active, expired, banned, inactive
    sub_type = Column(String, nullable=True)  # 1_month_rf, 3_month_rf, etc.
    
    # Связь с платежами
    payments = relationship("Payment", back_populates="user")


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # Связь с User
    telegram_id = Column(BigInteger, index=True)  # Для быстрого поиска
    status = Column(String, default='Pending')  # Pending, Completed, Failed, Cancelled
    amount = Column(Integer, nullable=False)  # Сумма в рублях
    currency = Column(String, default='RUB')
    description = Column(Text, nullable=True)
    subscription_type = Column(String, nullable=True)  # 1_month_rf, 3_month_rf, etc.
    cloudpayments_transaction_id = Column(String, nullable=True)  # ID транзакции от CloudPayments
    invoice_id = Column(String, nullable=True)  # ID заказа
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Связь с пользователем
    user = relationship("User", back_populates="payments")