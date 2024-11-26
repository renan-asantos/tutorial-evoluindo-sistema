from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


@table_registry.mapped_as_dataclass
class Genre:
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
    )
    movies: Mapped[list['Movie']] = relationship(
        init=False,
        back_populates='genre',
        cascade='all, delete-orphan',
    )


@table_registry.mapped_as_dataclass
class Movie:
    __tablename__ = 'movie'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    director: Mapped[str]
    year: Mapped[int]

    genre_id: Mapped[int] = mapped_column(ForeignKey('genre.id'))

    genre: Mapped[Genre] = relationship(
        init=False,
        back_populates='movies',
    )

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
    )
