# Create Pydantic schemas for:
# - CustomerCreate, CustomerRead
# - TicketCreate, TicketRead
# - ResponseCreate, ResponseRead
# Enable from_attributes for read schemas.
from pydantic import BaseModel, ConfigDict
from datetime import datetime   

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TicketBase(BaseModel):
    subject: str
    message: str
    status: str = "open"
    customer_id: int

class TicketCreate(TicketBase):
    pass

class TicketRead(TicketBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ResponseBase(BaseModel):
    ticket_id: int
    response_text: str

class ResponseCreate(ResponseBase):
    pass

class ResponseRead(ResponseBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

        