from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

class TransactionBase(BaseModel):
    tx_hash: str
    from_address: str
    to_address: str
    value: Decimal
    block_number: int
    status: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class TransactionFilter(BaseModel):
    address: Optional[str] = None
    start_block: Optional[int] = None
    end_block: Optional[int] = None