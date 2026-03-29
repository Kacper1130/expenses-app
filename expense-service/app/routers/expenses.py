from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.users import get_user_name
from app.settlement import compute_group_balances, calculate_debts

router = APIRouter(prefix="/api/expenses/groups", tags=["expenses"])


def get_current_user(x_user_id: str = Header(...)):
    return x_user_id


def check_membership(group_id: str, user_id: str, db: Session):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupa nie istnieje")
    membership = db.query(models.GroupMember).filter(
        models.GroupMember.group_id == group_id,
        models.GroupMember.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Nie jesteś członkiem tej grupy")
    return group


@router.post("/{group_id}/expenses", response_model=schemas.ExpenseResponse, status_code=201)
async def add_expense(
    group_id: str,
    expense_data: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    check_membership(group_id, user_id, db)

    # Pobierz wszystkich członków grupy — wydatek dzielony między WSZYSTKICH
    members = db.query(models.GroupMember).filter(
        models.GroupMember.group_id == group_id
    ).all()
    member_ids = [m.user_id for m in members]

    # Podziel kwotę po równo, zaokrąglij do 2 miejsc
    share = round(expense_data.amount / len(member_ids), 2)

    # Zapisz wydatek
    new_expense = models.Expense(
        group_id=group_id,
        paid_by=user_id,
        amount=expense_data.amount,
        description=expense_data.description
    )
    db.add(new_expense)
    db.flush()  # potrzebujemy new_expense.id dla splitów

    # Zapisz podział — jeden wiersz na osobę
    for member_id in member_ids:
        split = models.ExpenseSplit(
            expense_id=new_expense.id,
            user_id=member_id,
            amount=share
        )
        db.add(split)

    db.commit()
    db.refresh(new_expense)

    # Pobierz imię płacącego i zwróć odpowiedź z podziałem
    paid_by_name = await get_user_name(new_expense.paid_by)

    split_details = []
    for split in new_expense.splits:
        name = await get_user_name(split.user_id)
        split_details.append(schemas.SplitDetail(user_name=name, amount=split.amount))

    return schemas.ExpenseResponse(
        id=new_expense.id,
        group_id=new_expense.group_id,
        paid_by=paid_by_name,
        amount=new_expense.amount,
        description=new_expense.description,
        created_at=new_expense.created_at,
        splits=split_details
    )


@router.get("/{group_id}/expenses", response_model=list[schemas.ExpenseResponse])
async def get_expenses(
    group_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    check_membership(group_id, user_id, db)

    expenses = db.query(models.Expense).filter(
        models.Expense.group_id == group_id
    ).order_by(models.Expense.created_at.desc()).all()

    # Zbierz wszystkie unikalne ID userów (płacący + osoby z podziałów)
    all_user_ids = set()
    for e in expenses:
        all_user_ids.add(e.paid_by)
        for s in e.splits:
            all_user_ids.add(s.user_id)

    # Pobierz imiona wszystkich naraz
    names: dict[str, str] = {}
    for uid in all_user_ids:
        names[uid] = await get_user_name(uid)

    result = []
    for expense in expenses:
        split_details = [
            schemas.SplitDetail(user_name=names.get(s.user_id, s.user_id), amount=s.amount)
            for s in expense.splits
        ]
        result.append(schemas.ExpenseResponse(
            id=expense.id,
            group_id=expense.group_id,
            paid_by=names.get(expense.paid_by, expense.paid_by),
            amount=expense.amount,
            description=expense.description,
            created_at=expense.created_at,
            splits=split_details
        ))

    return result


@router.get("/{group_id}/balances", response_model=schemas.BalanceSummary)
async def get_balances(
    group_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Zwraca kto komu ile winien w tej grupie.
    Używa algorytmu minimalizacji długów z settlement.py
    """
    check_membership(group_id, user_id, db)

    # Pobierz wszystkich członków
    members = db.query(models.GroupMember).filter(
        models.GroupMember.group_id == group_id
    ).all()
    member_ids = [m.user_id for m in members]

    # Pobierz wydatki z podziałami
    expenses = db.query(models.Expense).filter(
        models.Expense.group_id == group_id
    ).all()

    # Oblicz salda
    balances = compute_group_balances(expenses, member_ids)

    # Zamień salda na listę konkretnych długów
    transactions = calculate_debts(balances)

    # Pobierz imiona wszystkich
    names: dict[str, str] = {}
    for uid in member_ids:
        names[uid] = await get_user_name(uid)

    # Zbuduj odpowiedź
    debts = [
        schemas.DebtEntry(
            from_user=names.get(debtor, debtor),
            to_user=names.get(creditor, creditor),
            amount=amount
        )
        for debtor, creditor, amount in transactions
    ]

    return schemas.BalanceSummary(
        debts=debts,
        settled=len(debts) == 0
    )
