from sqlalchemy import Column, Float, Integer, String, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class TopWallets(Base):
    __tablename__ = 'top_wallet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_address = Column(String, unique=True, nullable=False)
    transaction_volume = Column(Float, nullable=False, default=0.0)
    total_transactions = Column(Integer, nullable=False, default=0)
    total_value = Column(Float, nullable=False)

    # Relationships
    wallet = relationship("wallet", back_populates="top_wallet")
