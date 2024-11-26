from fastapi import FastAPI

from src.routers.genre import (
    router as genre_router,
)
from src.routers.movie import (
    router as movie_router,
)

app = FastAPI()


app.include_router(genre_router)
app.include_router(movie_router)
