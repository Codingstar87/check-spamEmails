from fastapi import APIRouter, Response, Request
from src.controllers.authcontrollers import create_user, user_login, get_user_by_session
from src.models.models import UserCreate, UserLogin
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

@router.post("/register")
@limiter.limit("5/minute")
async def register_user(request: Request, user: UserCreate, response: Response):
    return create_user(user, response)



@router.post("/login")
async def login_user(request: Request,data: UserLogin, response: Response):
    return user_login(data,response)




@router.get("/user")
async def get_user_info(request: Request):
    return get_user_by_session(request)


@router.get("/health")
async def health(request:Request):
    return "ok"
