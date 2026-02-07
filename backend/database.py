from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create the local SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./guide.db"

# 2. Connect to it (check_same_thread=False is needed for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create the Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class for all models
Base = declarative_base()

# 5. Dependency helper (we use this in every API endpoint)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()