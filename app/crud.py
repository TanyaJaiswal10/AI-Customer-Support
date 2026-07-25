# Write CRUD functions using SQLAlchemy for:
# Customers:
# - create_customer, get_customer, get_customers, update_customer, delete_customer
# Tickets:
# - create_ticket, get_ticket, get_tickets, update_ticket, delete_ticket
# Responses:
# - create_response, get_responses_by_ticket
from sqlalchemy.orm import Session
from app import models, schemas
# Customer CRUD
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()
def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db_customer.name = customer.name
        db_customer.email = customer.email
        db.commit()
        db.refresh(db_customer)
    return db_customer
def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer
# Ticket CRUD
def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        message=ticket.message,
        status=ticket.status
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
def get_tickets(db: Session, skip: int = 0, limit: int =
    100):
        return db.query(models.Ticket).offset(skip).limit(limit).all()
def update_ticket(db: Session, ticket_id: int, ticket: schemas.TicketCreate):
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket:
        db_ticket.customer_id = ticket.customer_id
        db_ticket.subject = ticket.subject
        db_ticket.message = ticket.message
        db_ticket.status = ticket.status
        db.commit()
        db.refresh(db_ticket)
    return db_ticket
def delete_ticket(db: Session, ticket_id: int):
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
    return db_ticket
# Response CRUD
def create_response(db: Session, response: schemas.ResponseCreate):
    db_response = models.Response(
        ticket_id=response.ticket_id,
        response_text=response.response_text
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response
def get_responses_by_ticket(db: Session, ticket_id: int):
    return db.query(models.Response).filter(models.Response.ticket_id == ticket_id).all()

    