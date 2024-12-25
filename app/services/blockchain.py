# app/services/blockchain.py
from web3 import Web3
from typing import List, Optional
from app.core.config import settings
from app.schemas.transaction import TransactionCreate
import logging

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))
        self.MAX_BLOCKS = 10  # Limit to last 10 blocks for testing
        
    async def get_latest_block(self) -> int:
        return self.w3.eth.block_number
    
    async def get_transaction(self, tx_hash: str) -> Optional[TransactionCreate]:
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            if tx is None or tx_receipt is None:
                return None

            return TransactionCreate(
                tx_hash=tx_hash,
                from_address=tx['from'],
                to_address=tx['to'] if tx.get('to') else '',
                value=Web3.from_wei(tx['value'], 'ether'),
                block_number=tx['blockNumber'],
                status='success' if tx_receipt['status'] == 1 else 'failed'
            )
        except Exception as e:
            logging.error(f"Error fetching transaction {tx_hash}: {str(e)}")
            return None

    async def get_address_transactions(
        self,
        address: str,
        start_block: Optional[int] = None,
        end_block: Optional[int] = None
    ) -> List[TransactionCreate]:
        current_block = self.w3.eth.block_number
        
        # If no start_block provided, use last MAX_BLOCKS blocks
        if not start_block:
            start_block = current_block - self.MAX_BLOCKS
        
        # If no end_block provided, use current block
        if not end_block:
            end_block = current_block
            
        # Ensure we're not scanning too many blocks
        if end_block - start_block > self.MAX_BLOCKS:
            start_block = end_block - self.MAX_BLOCKS

        logging.info(f"Scanning blocks from {start_block} to {end_block}")
        
        transactions = []
        address = address.lower()

        try:
            for block_num in range(start_block, end_block + 1):
                logging.info(f"Scanning block {block_num}")
                block = self.w3.eth.get_block(block_num, full_transactions=True)
                
                for tx in block.transactions:
                    # Check if transaction involves our address
                    tx_from = tx['from'].lower() if tx.get('from') else ''
                    tx_to = tx['to'].lower() if tx.get('to') else ''
                    
                    if address in [tx_from, tx_to]:
                        tx_data = await self.get_transaction(tx['hash'].hex())
                        if tx_data:
                            transactions.append(tx_data)
                            
                if len(transactions) >= 100:  # Limit total transactions
                    break
                    
        except Exception as e:
            logging.error(f"Error scanning blocks: {str(e)}")
            
        return transactions

# app/services/blockchain.py
# from web3 import Web3
# from typing import List, Optional
# from app.core.config import settings
# from app.schemas.transaction import TransactionCreate

# class BlockchainService:
#     def __init__(self):
#         self.w3 = Web3(Web3.HTTPProvider(settings.ETHEREUM_RPC_URL))
    
#     async def get_latest_block(self) -> int:
#         return self.w3.eth.block_number
    
#     async def get_transaction(self, tx_hash: str) -> Optional[TransactionCreate]:
#         try:
#             tx = self.w3.eth.get_transaction(tx_hash)
#             tx_receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
#             return TransactionCreate(
#                 tx_hash=tx_hash,
#                 from_address=tx['from'],
#                 to_address=tx['to'],
#                 value=Web3.from_wei(tx['value'], 'ether'),
#                 block_number=tx['blockNumber'],
#                 status='success' if tx_receipt['status'] == 1 else 'failed'
#             )
#         except Exception as e:
#             print(f"Error fetching transaction {tx_hash}: {str(e)}")
#             return None

#     async def get_address_transactions(
#         self,
#         address: str,
#         start_block: Optional[int] = None,
#         end_block: Optional[int] = None
#     ) -> List[TransactionCreate]:
#         if not start_block:
#             start_block = self.w3.eth.block_number - 1000  # Last 1000 blocks by default
#         if not end_block:
#             end_block = self.w3.eth.block_number

#         transactions = []
#         for block_num in range(start_block, end_block + 1):
#             block = self.w3.eth.get_block(block_num, full_transactions=True)
#             for tx in block.transactions:
#                 if tx['from'].lower() == address.lower() or (tx['to'] and tx['to'].lower() == address.lower()):
#                     tx_data = await self.get_transaction(tx['hash'].hex())
#                     if tx_data:
#                         transactions.append(tx_data)
        
#         return transactions