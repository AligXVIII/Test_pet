from pydantic import BaseModel
from typing import List, Optional, Literal

class Category(BaseModel):
    id: int
    name: str

class Tag(BaseModel):
    id: int
    name: str

class Pet(BaseModel):
    id: int  
    name: str  
    category: Optional[Category] = None
    photoUrls: Optional[List[str]] = None
    tags: Optional[List[Tag]] = None
    status: Literal["available", "pending", "sold"]
