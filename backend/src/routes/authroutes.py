from fastapi import APIRouter, Response, Request
from src.controllers.authcontrollers import create_user, user_login, get_user_by_session
from src.models.models import UserCreate, UserLogin
from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

@router.post("/register")
async def register_user(user: UserCreate, response: Response):
    return create_user(user, response)


@router.post("/login")
async def login_user(data: UserLogin):
    return user_login(data)




@router.get("/user")
@limiter.limit("3/minute")
async def get_user_info(request: Request):
    return get_user_by_session(request)


@router.get("/health")
async def health(request:Request):
    return "ok"
