#app/models/wallet.py
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True, index=True)
    address=Column(String,unique=True,nullable=True)
    balance=Column(Integer,nullable=False,default=0.0)

    transaction_sent=relationship("transaction",foreign_keys='transation.from_address',back_populates="sender_wallet")
    transactions_received = relationship("transaction", foreign_keys='transaction.to_address', back_populates="receiver_wallet")
    token_transfers_sent = relationship("token_transfer", foreign_keys='token_transfer.from_address')
    token_transfers_received = relationship("token_transfer", foreign_keys='token_transfer.to_address')
    wallet_activity = relationship("wallet_activity", back_populates="wallet")
    top_wallet = relationship("top_wallet", back_populates="wallet")