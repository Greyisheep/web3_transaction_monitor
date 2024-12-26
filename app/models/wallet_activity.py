from sqlalchemy import Column, Float, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class WalletActivity(Base):
    __tablename__ = 'wallet_activity'

    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_address = Column(String, unique=True, nullable=False)
    total_transactions = Column(Integer, nullable=False, default=0)
    total_ether_sent = Column(Float, nullable=False, default=0.0)
    total_ether_received = Column(Float, nullable=False, default=0.0)

    # Relationships
    wallet = relationship("wallet", back_populates="wallet_activity")