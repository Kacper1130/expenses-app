from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@expense-db:5432/expense_db"

settings = Settings()

# Silnik bazy danych - to jest nasze "połączenie" z Postgresem
engine = create_engine(settings.database_url)

# Fabryka sesji - każde zapytanie do bazy odbywa się przez sesję
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Klasa bazowa dla wszystkich modeli (tabel)
class Base(DeclarativeBase):
    pass


# Funkcja pomocnicza - daje nam sesję bazy i automatycznie ją zamyka po użyciu
def get_db():
    db = SessionLocal()
    try:
        yield db       # "yield" zamiast "return" - sesja żyje tylko podczas jednego zapytania HTTP
    finally:
        db.close()     # zawsze zamknij sesję, nawet jak wystąpił błąd
