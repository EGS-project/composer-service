from src.database import SessionLocal


def database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
