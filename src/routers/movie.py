from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud import create, delete, get_all, get_offset, get_one, update
from src.database import get_session
from src.models import Movie
from src.routers.schema import (
    Message,
    MovieInSchema,
    MovieOutSchema,
    MoviePartialUpdateSchema,
    PageMovieSchema,
)

router = APIRouter(prefix='/movie', tags=['movies'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=MovieOutSchema
)
def create_movie(
    movie: MovieInSchema,
    session: Session = Depends(get_session),
):
    if movie := create(session, Movie, movie):
        return movie
    raise HTTPException(HTTPStatus.BAD_REQUEST, detail='Movie already exists')


@router.get('/', response_model=list[MovieOutSchema])
def read_movies(session: Session = Depends(get_session)):
    return get_all(session, Movie)


@router.get('/pages/', response_model=PageMovieSchema)
def read_movies_by_page(
    page: int = 1, limit: int = 100, session: Session = Depends(get_session)
):
    movies = get_offset(session, Movie, page - 1, limit)

    return {'page': page, 'limit': limit, 'movies': movies}


@router.get('/{id}/', response_model=MovieOutSchema)
def read_movies(id: int, session: Session = Depends(get_session)):
    if movie := get_one(session, Movie, id):
        return movie

    raise HTTPException(HTTPStatus.NOT_FOUND, detail='Movie not found')


@router.put('/{id}/', response_model=MovieOutSchema)
def update_movie(
    id: int,
    movie_to_update: MovieInSchema,
    session: Session = Depends(get_session),
):
    movie, message = update(session, Movie, id, movie_to_update)
    if movie:
        return movie
    raise HTTPException(HTTPStatus.NOT_FOUND, detail=f'Movie {message}')


@router.patch(
    '/{id}/',
    response_model=MovieOutSchema,
)
def partial_update_movie(
    id: int,
    movie_to_update: MoviePartialUpdateSchema,
    session: Session = Depends(get_session),
):
    movie, message = update(session, Movie, id, movie_to_update)
    if movie:
        return movie
    raise HTTPException(HTTPStatus.NOT_FOUND, detail=f'Movie {message}')


@router.delete('/{id}/', status_code=HTTPStatus.OK, response_model=Message)
def delete_movie(id: int, session: Session = Depends(get_session)):
    if delete(session, Movie, id):
        return {'message': 'Movie deleted'}

    raise HTTPException(HTTPStatus.NOT_FOUND, detail='Movie not found')
