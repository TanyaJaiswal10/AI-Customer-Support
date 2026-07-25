# Create FastAPI routes for AI features:
# POST /ai/summarize-ticket/{ticket_id}
# POST /ai/analyze-sentiment/{ticket_id}
# POST /ai/suggest-reply/{ticket_id}
# Fetch ticket from database.
# Pass ticket message to AI functions.
# Return AI result as JSON.
# Add error handling if ticket not found.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, ai
from app.database import get_db
router = APIRouter()
@router.post("/summarize-ticket/{ticket_id}")
def summarize_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    summary = ai.summarize_ticket(db_ticket.message)
    return {"summary": summary}
@router.post("/analyze-sentiment/{ticket_id}")
def analyze_sentiment(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    result = ai.analyze_sentiment(db_ticket.message)
    return { "result": result}
@router.post("/suggest-reply/{ticket_id}")
def suggest_reply(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    reply = ai.suggest_reply(db_ticket.message)
    return {"suggested_reply": reply}
