from backend import BASE_PATH
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .sample_data import customers, rooms

DB_NAME = "hotel.db"
DB_PATH = BASE_PATH / DB_NAME

# SQLALCHEMY_DATABASE_URL = "sqlite:///./hotel.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    if not DB_PATH.exists():
        logger.info("Database not exists. Creating database...")
        Base.metadata.create_all(engine)
        db = SessionLocal()
        db.add_all(customers)
        db.add_all(rooms)
        db.commit()
        db.close()
        logger.info("Database created.")
    else:
        logger.info("Database is already exists.")
