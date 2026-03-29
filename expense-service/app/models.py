from datetime import datetime
import random
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


def generate_group_code():
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(random.choices(chars, k=5))


class Group(Base):
    __tablename__ = "groups"

    id = Column(String(5), primary_key=True, default=generate_group_code)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("GroupMember", back_populates="group", cascade="all, delete")
    expenses = relationship("Expense", back_populates="group", cascade="all, delete")


class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True)
    group_id = Column(String(5), ForeignKey("groups.id"), nullable=False)
    user_id = Column(String, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("group_id", "user_id"),)

    group = relationship("Group", back_populates="members")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    group_id = Column(String(5), ForeignKey("groups.id"), nullable=False)
    paid_by = Column(String, nullable=False)   # user_id osoby która zapłaciła
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="expenses")
    splits = relationship("ExpenseSplit", back_populates="expense", cascade="all, delete")


class ExpenseSplit(Base):
    """
    Kto jest winny ile za dany wydatek.
    Przy wydatku 60zł na 3 osoby → 3 wiersze po 20zł każdy.
    """
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id = Column(String, nullable=False)   # kto jest winny
    amount = Column(Float, nullable=False)      # ile jest winny

    expense = relationship("Expense", back_populates="splits")
