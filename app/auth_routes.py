from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .supabase_client import supabase

router = APIRouter()


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/auth/signup", status_code=201)
def signup(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email and password required")

    try:
        result = supabase.auth.sign_up({"email": data.email, "password": data.password})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"user": result.user}

@router.post("/auth/login")
def login(data: AuthRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Envalid email or password")

    try:
        result = supabase.auth.sign_in_with_password({"email": data.email, "password": data.password})
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    return {"access_token": result.session.access_token}