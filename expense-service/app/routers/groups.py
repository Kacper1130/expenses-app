from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/expenses/groups", tags=["groups"])


def get_current_user(x_user_id: str = Header(...)):
    return x_user_id


@router.post("", response_model=schemas.GroupResponse, status_code=201)
def create_group(
    group_data: schemas.GroupCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    new_group = models.Group(
        name=group_data.name,
        description=group_data.description,
        owner_id=user_id
    )
    db.add(new_group)
    db.flush()

    member = models.GroupMember(group_id=new_group.id, user_id=user_id)
    db.add(member)

    db.commit()
    db.refresh(new_group)
    return new_group


@router.get("", response_model=list[schemas.GroupWithMembers])
def get_my_groups(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    memberships = db.query(models.GroupMember).filter(
        models.GroupMember.user_id == user_id
    ).all()

    result = []
    for membership in memberships:
        group = membership.group
        member_count = db.query(models.GroupMember).filter(
            models.GroupMember.group_id == group.id
        ).count()

        result.append(schemas.GroupWithMembers(
            id=group.id,
            name=group.name,
            description=group.description,
            owner_id=group.owner_id,
            created_at=group.created_at,
            member_count=member_count
        ))

    return result


@router.post("/{group_id}/join", response_model=schemas.MessageResponse)
def join_group(
    group_id: str,           # było int, teraz str
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupa nie istnieje")

    existing = db.query(models.GroupMember).filter(
        models.GroupMember.group_id == group_id,
        models.GroupMember.user_id == user_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Już jesteś członkiem tej grupy")

    new_member = models.GroupMember(group_id=group_id, user_id=user_id)
    db.add(new_member)
    db.commit()

    return {"message": f"Dołączyłeś do grupy '{group.name}'"}
