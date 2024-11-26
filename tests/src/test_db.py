from dataclasses import asdict

from sqlalchemy import select

from src.models import Genre, Movie


def test_create_genre(session, mock_db_time):
    with mock_db_time(model=Genre) as time:
        new_genre = Genre(name='Fantasia')
        session.add(new_genre)

        session.commit()

    genre = session.scalar(select(Genre).where(Genre.name == 'Fantasia'))

    assert asdict(genre) == {
        'id': 1,
        'name': 'Fantasia',
        'created_at': time,
        'updated_at': time,
        'movies': [],
    }


def test_create_movie(session, mock_db_time, genre: Genre):
    with mock_db_time(model=Movie) as time:
        new_movie = Movie(
            title='A viagem de Chihiro',
            director='Hayao Miyasaki',
            year=2003,
            genre_id=genre.id,
        )
        session.add(new_movie)

        session.commit()
        session.refresh(new_movie)

    movie = session.scalar(
        select(Movie).where(Movie.title == 'A viagem de Chihiro')
    )
    genre = session.scalar(select(Genre).where(Genre.id == genre.id))

    assert movie in genre.movies
