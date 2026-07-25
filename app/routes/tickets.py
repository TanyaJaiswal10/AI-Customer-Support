# Create a FastAPI router for Ticket CRUD APIs.
# Endpoints:
# POST /tickets
# GET /tickets
# GET /tickets/{id}
# PUT /tickets/{id}
# DELETE /tickets/{id}
# Use database dependency injection.
# Validate that customer exists when creating ticket.
# Add basic error handling.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
router = APIRouter()
@router.post("/", response_model=schemas.TicketRead)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    # Validate customer exists
    db_customer = crud.get_customer(db, customer_id=ticket.customer_id)
    if db_customer is None:
        raise HTTPException(status_code=400, detail="Customer not found")
    return crud.create_ticket(db=db, ticket=ticket)
@router.get("/", response_model=list[schemas.TicketRead])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tickets(db, skip=skip, limit=limit)
@router.get("/{ticket_id}", response_model=schemas.TicketRead)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
@router.put("/{ticket_id}", response_model=schemas.TicketRead)
def update_ticket(ticket_id: int, ticket: schemas.TicketCreate, db: Session =
    Depends(get_db)):
        db_ticket = crud.update_ticket(db, ticket_id=ticket_id, ticket=ticket)
        if db_ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return db_ticket
@router.delete("/{ticket_id}", response_model=schemas.TicketRead)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.delete_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
