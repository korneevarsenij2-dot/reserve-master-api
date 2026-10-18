from datetime import datetime
from pydantic import BaseModel, Field

class TableCreate(BaseModel):
    number: int = Field(gt=0, description="номер стола")
    capacity: int = Field(gt=0, le=20,
    description="вместимость (от 1 до 20 мест)")

class TableResponse(BaseModel):
    id: int
    number: int
    capacity: int
    model_config = {"from_attributes":True}

class BookingCreate(BaseModel):
    table_id: int = Field(gt=0)
    guest_name: str = Field(min_length=2, max_length=100)
    starts_at: datetime

class BookingResponse(BaseModel):
    id: int = Field(gt=0)
    table_id: int
    guest_name: str
    starts_at: datetime
    model_config = {"from_attributes":True}

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = {"from_attributes":True}

class Token(BaseModel):
    access_token: str
    token_type: str

