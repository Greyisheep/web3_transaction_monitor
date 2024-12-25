# app/models/transaction.py
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, unique=True, index=True)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    value = Column(Numeric(precision=36, scale=18))  # For ETH values
    block_number = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)  # 'success' or 'failed'