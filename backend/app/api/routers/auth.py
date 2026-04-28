from fastapi import APIRouter, Depends, HTTPException, status, Security
from datetime import timedelta
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.db.mongodb import get_db
from app.schemas.user import UserCreate, UserResponse, Token, LoginRequest, UserResponseWithToken
from app.models.user import UserInDB
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponseWithToken)
async def register(user_in: UserCreate, db = Depends(get_db)):
    user = await db["users"].find_one({"email": user_in.email})
    if user:
        raise HTTPException(
            status_code=400,
            detail="Bu email adresine sahip bir kullanıcı zaten mevcut.",
        )

    user_dict = user_in.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

    new_user = UserInDB(**user_dict)
    result = await db["users"].insert_one(new_user.model_dump(by_alias=True, exclude={"id"}))

    created_user = await db["users"].find_one({"_id": result.inserted_id})
    created_user["id"] = str(created_user.pop("_id"))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(result.inserted_id), expires_delta=access_token_expires
    )

    user_response = UserResponse(
        id=created_user["id"],
        email=created_user["email"],
        full_name=created_user.get("full_name"),
        is_active=created_user.get("is_active", True)
    )

    return {
        "user": user_response,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest, db = Depends(get_db)):
    user = await db["users"].find_one({"email": login_request.email})
    if not user or not verify_password(login_request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email veya şifre hatalı"
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user["_id"]), expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: UserInDB = Security(get_current_user)):
    user_dict = current_user.model_dump()
    user_dict["id"] = str(user_dict.pop("id", current_user.id))
    return user_dict
