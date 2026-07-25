# Setup SQLite database using SQLAlchemy.
# Create engine, SessionLocal, and Base.
# Configure database URL as sqlite:///./support.db
# Provide a get_db dependency function for FastAPI.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite:///./support.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        