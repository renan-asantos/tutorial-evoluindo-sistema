from http import HTTPStatus


def test_create_movie(client, genre):
    response = client.post(
        '/movie',
        json={
            'title': 'A viagem de Chihiro',
            'year': 2001,
            'director': 'Hayao Miyazaki',
            'genre_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'A viagem de Chihiro',
        'year': 2001,
        'director': 'Hayao Miyazaki',
        'genre': {'name': 'Fantasia', 'id': 1},
        'id': 1,
    }


def test_get_movies_empty(client, genre):
    response = client.get(
        '/movie',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_movies(client, genre, movie):
    response = client.get(
        '/movie',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'title': 'A viagem de Chihiro',
            'year': 2001,
            'director': 'Hayao Miyazaki',
            'genre': {'name': 'Fantasia', 'id': 1},
            'id': 1,
        }
    ]


def test_get_movies_more_than_one_movie(client, genre, movie, other_movie):
    response = client.get(
        '/movie',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'title': 'A viagem de Chihiro',
            'year': 2001,
            'director': 'Hayao Miyazaki',
            'genre': {'name': 'Fantasia', 'id': 1},
            'id': 1,
        },
        {
            'title': 'O castelo animado',
            'year': 2005,
            'director': 'Hayao Miyazaki',
            'genre': {'name': 'Fantasia', 'id': 1},
            'id': 2,
        },
    ]


def test_get_movies_pages_empty(client):
    response = client.get(
        '/movie/pages?limit=1',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'page': 1,
        'limit': 1,
        'movies': [],
    }


def test_get_movies_pages(client, movie, other_movie):
    response = client.get(
        '/movie/pages/',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'page': 1,
        'limit': 100,
        'movies': [
            {
                'title': 'A viagem de Chihiro',
                'year': 2001,
                'director': 'Hayao Miyazaki',
                'genre': {'name': 'Fantasia', 'id': 1},
                'id': 1,
            },
            {
                'title': 'O castelo animado',
                'year': 2005,
                'director': 'Hayao Miyazaki',
                'genre': {'name': 'Fantasia', 'id': 1},
                'id': 2,
            },
        ],
    }


def test_get_one_movie(client, genre, movie):
    response = client.get(
        '/movie/1/',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'A viagem de Chihiro',
        'year': 2001,
        'director': 'Hayao Miyazaki',
        'genre': {'name': 'Fantasia', 'id': 1},
        'id': 1,
    }


def test_get_movie_not_found(client):
    response = client.get(
        '/movie/1/',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Movie not found'}


def test_update_movie(client, genre, movie):
    response = client.put(
        '/movie/1/',
        json={
            'title': 'O menino e a garça',
            'year': 2023,
            'director': 'Hayao Miyazaki',
            'genre_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'O menino e a garça',
        'year': 2023,
        'director': 'Hayao Miyazaki',
        'genre': {'name': 'Fantasia', 'id': 1},
        'id': 1,
    }


def test_update_movie_failed_by_not_found(client, genre):
    response = client.put(
        '/movie/1/',
        json={
            'title': 'O menino e a garça',
            'year': 2023,
            'director': 'Hayao Miyazaki',
            'genre_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Movie not found'}


def test_partial_update_movie(client, genre, movie):
    response = client.patch(
        '/movie/1/',
        json={
            'title': 'O menino e a garça',
            'year': 2023,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'title': 'O menino e a garça',
        'year': 2023,
        'director': 'Hayao Miyazaki',
        'genre': {'name': 'Fantasia', 'id': 1},
        'id': 1,
    }


def test_partial_update_movie_failed_by_not_found(client, genre):
    response = client.patch(
        '/movie/1/',
        json={
            'title': 'O menino e a garça',
            'year': 2023,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Movie not found'}


def test_delete_movie(client, movie):
    response = client.delete(
        '/movie/1/',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Movie deleted'}


def test_delete_movie_fail_by_not_found(client):
    response = client.delete(
        '/movie/1/',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Movie not found'}
