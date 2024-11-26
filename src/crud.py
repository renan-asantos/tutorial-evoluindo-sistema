from sqlalchemy import select
from sqlalchemy.exc import (
    IntegrityError,
)
from sqlalchemy.orm import Session


def create(session: Session, model, data):
    try:
        obj = model(**data.model_dump())
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except IntegrityError:
        None


def get_all(session: Session, model):
    query = select(model)
    return session.scalars(query).all()


def get_offset(session: Session, model, offset, limit):
    query = select(model).offset(offset * limit).limit(limit)
    return session.scalars(query).all()


def get_one(session: Session, model, id: int):
    query = select(model).where(model.id == id)
    return session.scalars(query).one_or_none()


def update(session: Session, model, id: int, data):
    query = select(model).where(model.id == id)
    obj = session.scalars(query).one_or_none()
    if obj is None:
        return None, 'not found'
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(obj, attr, value)
    try:
        session.commit()
        session.refresh(obj)
        return obj, None
    except IntegrityError:
        return None, 'already exists'


def delete(session: Session, model, id: int) -> bool:
    query = select(model).where(model.id == id)
    obj = session.scalars(query).one_or_none()

    if obj is None:
        return False

    session.delete(obj)
    session.commit()
    return True
