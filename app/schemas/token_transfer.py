from pydantic import BaseModel, Field
from datetime import datetime

class Token_transferBase(BaseModel):
    token_contract_address : str
    token_type: str
    from_address:str
    to_address:str
    tx_hash:str
    token_id:str
    value:int
   
class Token_transferBaseCreate (Token_transferBase):
    pass
class Token_transferBaseResposnse(Token_transferBase):
    id:int
    token_contract_address : str
    token_type: str
    from_address:str
    to_address:str
    tx_hash:str
    token_id:str
    value:int
class Token_transfer(Token_transferBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True