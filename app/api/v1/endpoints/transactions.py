# app/api/v1/endpoints/transactions.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_db
from app.schemas.transaction import Transaction, TransactionCreate, TransactionFilter
from app.services.blockchain import BlockchainService
from app.models.transaction import Transaction as TransactionModel

router = APIRouter()
blockchain_service = BlockchainService()

@router.get("/address/{address}/transactions", response_model=List[Transaction])
async def get_address_transactions(
    address: str,
    start_block: Optional[int] = Query(None, description="Starting block number"),
    end_block: Optional[int] = Query(None, description="Ending block number"),
    db: Session = Depends(get_db)
):
    try:
        # First check DB for existing transactions
        query = db.query(TransactionModel).filter(
            (TransactionModel.from_address.ilike(address)) |
            (TransactionModel.to_address.ilike(address))
        )
        
        if start_block:
            query = query.filter(TransactionModel.block_number >= start_block)
        if end_block:
            query = query.filter(TransactionModel.block_number <= end_block)
            
        existing_transactions = query.all()
        
        # If we have some transactions, return them
        if existing_transactions:
            return existing_transactions
            
        # If no transactions in DB, fetch from blockchain
        new_transactions = await blockchain_service.get_address_transactions(
            address,
            start_block,
            end_block
        )
        
        # Save new transactions to database
        db_transactions = []
        for tx_data in new_transactions:
            existing_tx = db.query(TransactionModel).filter(
                TransactionModel.tx_hash == tx_data.tx_hash
            ).first()
            
            if not existing_tx:
                db_tx = TransactionModel(**tx_data.dict())
                db.add(db_tx)
                db_transactions.append(db_tx)
        
        if db_transactions:
            db.commit()
            return db_transactions
            
        return []
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching transactions: {str(e)}"
        )

# # app/api/v1/endpoints/transactions.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from app.core.dependencies import get_db
# from app.schemas.transaction import Transaction, TransactionCreate, TransactionFilter
# from app.services.blockchain import BlockchainService
# from app.models.transaction import Transaction as TransactionModel

# router = APIRouter()
# blockchain_service = BlockchainService()

# @router.get("/transactions/{tx_hash}", response_model=Transaction)
# async def get_transaction(
#     tx_hash: str,
#     db: Session = Depends(get_db)
# ):
#     # Check if transaction exists in database
#     db_tx = db.query(TransactionModel).filter(TransactionModel.tx_hash == tx_hash).first()
#     if db_tx:
#         return db_tx

#     # If not in database, fetch from blockchain
#     tx_data = await blockchain_service.get_transaction(tx_hash)
#     if not tx_data:
#         raise HTTPException(status_code=404, detail="Transaction not found")
    
#     # Save to database
#     db_tx = TransactionModel(**tx_data.dict())
#     db.add(db_tx)
#     db.commit()
#     db.refresh(db_tx)
    
#     return db_tx

# @router.get("/address/{address}/transactions", response_model=List[Transaction])
# async def get_address_transactions(
#     address: str,
#     start_block: int = None,
#     end_block: int = None,
#     db: Session = Depends(get_db)
# ):
#     # Fetch new transactions from blockchain
#     tx_filter = TransactionFilter(
#         address=address,
#         start_block=start_block,
#         end_block=end_block
#     )
    
#     new_transactions = await blockchain_service.get_address_transactions(
#         address,
#         start_block,
#         end_block
#     )
    
#     # Save new transactions to database
#     for tx_data in new_transactions:
#         existing_tx = db.query(TransactionModel).filter(
#             TransactionModel.tx_hash == tx_data.tx_hash
#         ).first()
        
#         if not existing_tx:
#             db_tx = TransactionModel(**tx_data.dict())
#             db.add(db_tx)
    
#     db.commit()
    
#     # Query all transactions for the address
#     query = db.query(TransactionModel).filter(
#         (TransactionModel.from_address == address) |
#         (TransactionModel.to_address == address)
#     )
    
#     if start_block:
#         query = query.filter(TransactionModel.block_number >= start_block)
#     if end_block:
#         query = query.filter(TransactionModel.block_number <= end_block)
    
#     return query.all()