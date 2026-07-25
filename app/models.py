# Define SQLAlchemy models for:
# - Customer: id, name, email
# - Ticket: id, customer_id, subject, message, status, created_at
# - Response: id, ticket_id, response_text, created_at
# Use declarative base.
# Add relationships between Customer and Ticket, and Ticket and Response.
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    tickets = relationship("Ticket", back_populates="customer")
class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    subject = Column(String, index=True)
    message = Column(String)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    customer = relationship("Customer", back_populates="tickets")
    responses = relationship("Response", back_populates="ticket")
class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    response_text = Column(String)
    created_at = Column(DateTime)
    ticket = relationship("Ticket", back_populates="responses")

