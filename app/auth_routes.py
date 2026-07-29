from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel

from .supabase_client import supabase
from .auth_dependency import get_current_user

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

@router.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@router.get("/protected/profile")
def profile(user = Depends(get_current_user)):

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }

@router.get("/protected/dashboard")
def dashboard(user = Depends(get_current_user)):
    return {"message": f"Welcome {user.email}"}

@router.post("/auth/logout", status_code=204)
def logout(user = Depends(get_current_user)):
    supabase.auth.sign_out()
    return