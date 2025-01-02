from pydantic import BaseModel

class Wallet_activityBase(BaseModel):
    wallet_address : str
    total_transaction:int
    total_ether_sent:int
    total_ether_received:int
class   Wallet_activityCreate ( Wallet_activityBase):
    pass
class  Wallet_activityResponse( Wallet_activityBase):
    id:int
    wallet_address : str
    total_transaction:int
    total_ether_sent:int
    total_ether_received:int

class  Wallet_activity( Wallet_activityBase):
    id: int
    class Config:
        from_attributes = True