from sqlalchemy import create_engine
from core.config import settings
from sqlalchemy.orm import sessionmaker

# create engine instance
engine = create_engine(url=settings.SQLALCHEMY_DATABASE_URL,
                       connect_args={'check_same_thread': False})

# create session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
