# Create FastAPI app
# Add root endpoint
# Include routers for customers, tickets, ai_tools
from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes import customers, tickets, ai_tools    
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Customer Support AI API!"}
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(ai_tools.router, prefix="/ai-tools", tags=["ai-tools"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # or  for stricter
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
