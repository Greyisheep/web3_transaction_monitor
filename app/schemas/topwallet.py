from pydantic import BaseModel, Field

class TopwalletBase(BaseModel):
    wallet_address : str
    transaction_volume: int
    total_transaction:int
    total_value:int
class  TopwalletCreate (TopwalletBase):
    pass
class TopewalletResponse(TopwalletBase):
    id:int
    wallet_address : str
    transaction_volume: int
    total_transaction:int
    total_value:int

class Topwallet(TopwalletBase):
    id: int
    class Config:
        from_attributes = True