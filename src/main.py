from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles

from auth.base_config import auth_backend
from auth.models import User
from auth.schemas import UserRead, UserCreate

from auth.base_config import current_user, fastapi_users
from config import REDIS_HOST, REDIS_PORT

from operations.router import router as router_operation
from tasks.router import router as router_tasks

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from fastapi.middleware.cors import CORSMiddleware

from pages.router import router as router_pages
from chat.router import router as router_chat

from fastapi.responses import RedirectResponse

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Trading App"
)

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/")
def read_root():
    return RedirectResponse(url="/pages/search/string")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"


app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

