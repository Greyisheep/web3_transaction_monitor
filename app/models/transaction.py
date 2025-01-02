# app/models/transaction.py
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, unique=True, index=True)
    from_address = Column(String,ForeignKey('wallet.address'), index=True)
    to_address = Column(String,ForeignKey('wallet.address'), index=True)
    value = Column(Numeric(precision=36, scale=18))  # For ETH values
    block_number = Column(Integer)
    gas_fees = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)  # 'success' or 'failed'
    # Relationships
    sender_wallet = relationship("wallet", foreign_keys=[from_address], back_populates="transactions_sent")
    receiver_wallet = relationship("wallet", foreign_keys=[to_address], back_populates="transactions_received")
    token_transfers = relationship("token_transfer", back_populates="transaction")