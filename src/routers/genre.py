from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import create, delete, get_all, get_offset, get_one, update
from src.database import get_session
from src.models import Genre
from src.routers.schema import (
    GenreInSchema,
    GenreOutSchema,
    Message,
    PageGenreSchema,
)

router = APIRouter(prefix='/genre', tags=['genres'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=GenreOutSchema,
)
def create_genre(
    genre: GenreInSchema, session: Session = Depends(get_session)
):
    if genre := create(session, Genre, genre):
        return genre
    raise HTTPException(
        HTTPStatus.BAD_REQUEST,
        detail='Genre already exists',
    )


@router.get('/', response_model=list[GenreOutSchema])
def read_genres(session: Session = Depends(get_session)):
    return get_all(session, Genre)


@router.get('/pages/', response_model=PageGenreSchema)
def read_genres_by_page(
    page: int = 1, limit: int = 100, session: Session = Depends(get_session)
):
    genres = get_offset(session, Genre, page - 1, limit)

    return {'page': page, 'limit': limit, 'genres': genres}


@router.get('/{id}/', response_model=GenreOutSchema)
def read_genres(id: int, session: Session = Depends(get_session)):
    if genre := get_one(session, Genre, id):
        return genre

    raise HTTPException(HTTPStatus.NOT_FOUND, detail='Genre not found')


@router.put('/{id}/', response_model=GenreOutSchema)
def update_genre(
    id: int,
    genre_to_update: GenreInSchema,
    session: Session = Depends(get_session),
):
    genre, message = update(session, Genre, id, genre_to_update)
    if genre:
        return genre
    raise HTTPException(HTTPStatus.NOT_FOUND, detail=f'Genre {message}')


@router.patch('/{id}/', response_model=GenreOutSchema)
def partial_update_genre(
    id: int,
    genre_to_update: GenreInSchema,
    session: Session = Depends(get_session),
):
    genre, message = update(session, Genre, id, genre_to_update)
    if genre:
        return genre
    raise HTTPException(HTTPStatus.NOT_FOUND, detail=f'Genre {message}')


@router.delete('/{id}/', status_code=HTTPStatus.OK, response_model=Message)
def delete_genre(id: int, session: Session = Depends(get_session)):
    if delete(session, Genre, id):
        return {'message': 'Genre deleted'}

    raise HTTPException(HTTPStatus.NOT_FOUND, detail='Genre not found')
