from http import HTTPStatus


def test_create_genre(client):
    response = client.post(
        '/genre',
        json={
            'name': 'Fantasia',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'Fantasia',
        'id': 1,
    }


def test_create_fail_by_alread_exists(client, genre):
    response = client.post(
        '/genre',
        json={
            'name': 'Fantasia',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Genre already exists',
    }


def test_get_genres_empty(client):
    response = client.get(
        '/genre',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_genres(client, genre):
    response = client.get(
        '/genre',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'name': 'Fantasia',
            'id': 1,
        }
    ]


def test_get_genres_more_than_one_genre(client, genre, other_genre):
    response = client.get(
        '/genre',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'name': 'Fantasia',
            'id': 1,
        },
        {
            'name': 'Ficção',
            'id': 2,
        },
    ]


def test_get_genres_pages_empty(client):
    response = client.get(
        '/genre/pages?limit=1',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'page': 1,
        'limit': 1,
        'genres': [],
    }


def test_get_genres_pages(client, genre, other_genre):
    response = client.get(
        '/genre/pages?limit=1',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'page': 1,
        'limit': 1,
        'genres': [
            {
                'name': 'Fantasia',
                'id': 1,
            }
        ],
    }


def test_get_genres_pages_limit_greater_than_one(client, genre, other_genre):
    response = client.get(
        '/genre/pages?limit=2',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'page': 1,
        'limit': 2,
        'genres': [
            {
                'name': 'Fantasia',
                'id': 1,
            },
            {
                'name': 'Ficção',
                'id': 2,
            },
        ],
    }


def test_get_one_movie(client, genre):
    response = client.get(
        '/genre/1/',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Fantasia',
        'id': 1,
    }


def test_get_genre_not_found(client):
    response = client.get(
        '/genre/1/',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Genre not found'}


def test_total_update_genre(client, genre):
    response = client.put(
        '/genre/1/',
        json={
            'name': 'Terror',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Terror',
        'id': 1,
    }


def test_total_update_genre_fail_by_already_exists(client, genre, other_genre):
    response = client.put(
        '/genre/1/',
        json={
            'name': 'Ficção',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Genre already exists',
    }


def test_total_update_genre_fail_by_not_found(client):
    response = client.put(
        '/genre/1/',
        json={
            'name': 'Terror',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Genre not found'}


def test_partial_update_genre(client, genre):
    response = client.patch(
        '/genre/1/',
        json={
            'name': 'Terror',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'name': 'Terror',
        'id': 1,
    }


def test_total_update_genre_fail_by_already_exists(client, genre, other_genre):
    response = client.patch(
        '/genre/1/',
        json={
            'name': 'Ficção',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Genre already exists',
    }


def test_partial_update_genre_fail_by_not_found(client):
    response = client.patch(
        '/genre/1/',
        json={
            'name': 'Terror',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Genre not found'}


def test_delete_genre(client, genre):
    response = client.delete(
        '/genre/1/',
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Genre deleted'}


def test_delete_genre_fail_by_not_found(client):
    response = client.delete(
        '/genre/1/',
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Genre not found'}
