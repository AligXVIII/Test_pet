from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class Order(BaseModel):
    id: int  
    petId: int  
    quantity: int 
    shipDate: datetime
    status: Literal["placed", "approved", "delivered"]
    complete: bool