from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
class TokenTransfer(Base):
    __tablename__ = 'token_transfers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_contract_address = Column(String, nullable=False)
    token_type = Column(String, nullable=False)  # ERC-20 or ERC-721
    from_address = Column(String, ForeignKey('wallet.address'), nullable=False)
    to_address = Column(String, ForeignKey('wallet.address'), nullable=False)
    tx_hash = Column(String, ForeignKey('transactions.tx_hash'), nullable=False)
    token_id = Column(String, nullable=True)  # For ERC-721 (NFTs)
    value = Column(Float, nullable=True)  # For ERC-20
    timestamp = Column(DateTime, default=func.now())

    # Relationships
    sender_wallet = relationship("wallet", foreign_keys=[from_address], back_populates="token_transfers_sent")
    receiver_wallet = relationship("wallet", foreign_keys=[to_address], back_populates="token_transfers_received")
    transaction = relationship("transaction", back_populates="token_transfers")


