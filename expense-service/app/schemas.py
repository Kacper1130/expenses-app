from datetime import datetime
from pydantic import BaseModel, field_validator


# --- GRUPY ---

class GroupCreate(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Nazwa grupy nie może być pusta")
        return v


class GroupResponse(BaseModel):
    id: str
    name: str
    description: str | None
    owner_id: str
    created_at: datetime
    model_config = {"from_attributes": True}


class GroupWithMembers(GroupResponse):
    member_count: int


# --- WYDATKI ---

class ExpenseCreate(BaseModel):
    amount: float
    description: str

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("Kwota musi być większa od zera")
        return v

    @field_validator("description")
    @classmethod
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Opis wydatku nie może być pusty")
        return v


class SplitDetail(BaseModel):
    """Jeden wiersz podziału — czyja część i ile"""
    user_name: str
    amount: float


class ExpenseResponse(BaseModel):
    id: int
    group_id: str
    paid_by: str          # imię płacącego
    amount: float
    description: str
    created_at: datetime
    splits: list[SplitDetail] = []   # lista kto ile jest winny za ten wydatek

    model_config = {"from_attributes": True}


# --- ROZLICZENIA ---

class DebtEntry(BaseModel):
    """
    Jeden dług: 'Anna winna Kasi 35.50 zł'
    from_user = Anna, to_user = Kasia, amount = 35.50
    """
    from_user: str    # kto jest winny (imię)
    to_user: str      # komu jest winny (imię)
    amount: float     # ile


class BalanceSummary(BaseModel):
    """Pełne podsumowanie rozliczeń grupy"""
    debts: list[DebtEntry]         # lista długów do spłaty
    settled: bool                   # True jeśli wszyscy są kwita


# --- OGÓLNE ---

class MessageResponse(BaseModel):
    message: str
