from pydantic import BaseModel


class GenreInSchema(BaseModel):
    name: str


class GenreOutSchema(GenreInSchema):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        from_attributes = True


class PageGenreSchema(BaseModel):
    page: int = 1
    limit: int = 100
    genres: list[GenreOutSchema]


class MovieInSchema(BaseModel):
    title: str
    director: str
    year: int
    genre_id: int


class MovieBDSchema(MovieInSchema):
    genre_relationship: GenreOutSchema


class MovieOutSchema(BaseModel):
    id: int
    title: str
    director: str
    year: int
    # created_at: datetime
    # updated_at: datetime
    genre: GenreOutSchema

    class Config:
        from_attributes = True


class MoviePartialUpdateSchema(BaseModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None
    genre_id: int | None = None


class PageMovieSchema(BaseModel):
    page: int = 1
    limit: int = 100
    movies: list[MovieOutSchema]


class Message(BaseModel):
    message: str
