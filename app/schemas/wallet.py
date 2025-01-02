from pydantic import BaseModel
class WalletBase(BaseModel):
    address : str
    balance: int
class WalletCreate (WalletBase):
    pass

class WalletResponse(WalletBase):
    id:int
    address : str
    balance: int

class Wallet(WalletBase):
    id: int
    class Config:
        from_attributes = True