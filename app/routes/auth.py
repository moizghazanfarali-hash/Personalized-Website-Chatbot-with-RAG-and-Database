from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime

from app.database  import users_col
from app.security  import hash_password, verify_password, create_token, get_current_user
from app.models    import RegisterRequest, LoginRequest, AuthResponse, UserResponse

router = APIRouter(prefix="/api", tags=["Auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(req: RegisterRequest):
    if users_col.find_one({"email": req.email}):
        raise HTTPException(status_code=400, detail="This email already exist")

    hashed = hash_password(req.password)
    users_col.insert_one({
        "name":       req.name,
        "email":      req.email,
        "password":   hashed,
        "created_at": datetime.utcnow(),
    })

    token = create_token({"sub": req.email, "name": req.name})
    return AuthResponse(message="Account ban gaya!", token=token,
                        name=req.name, email=req.email)


@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest):
    user = users_col.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Email ya password galat hai")

    token = create_token({"sub": user["email"], "name": user["name"]})
    return AuthResponse(message="Login ho gaya!", token=token,
                        name=user["name"], email=user["email"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: str = Depends(get_current_user)):
    user = users_col.find_one({"email": current_user}, {"_id": 0, "password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User nahi mila")
    return UserResponse(name=user["name"], email=user["email"])
