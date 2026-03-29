from fastapi import FastAPI
from app.database import engine, Base
from app.routers import groups, expenses

# Tworzymy aplikację FastAPI
app = FastAPI(title="Expense Service")

# Tworzy wszystkie tabele w bazie jeśli jeszcze nie istnieją
# SQLAlchemy czyta nasze modele (models.py) i wykonuje CREATE TABLE
Base.metadata.create_all(bind=engine)

# Rejestrujemy routery - dodajemy nasze endpointy do aplikacji
app.include_router(groups.router)
app.include_router(expenses.router)


@app.get("/health")
def health_check():
    """Prosty endpoint do sprawdzenia czy serwis żyje. Używany przez Docker."""
    return {"status": "ok"}
