from pydantic import BaseModel
from typing import List, Any
from datetime import datetime

class QueryRequest(BaseModel):
    user_id: str
    query: str

class QueryResponse(BaseModel):
    query: str
    result: List[Any]
    
class UserRequest(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
