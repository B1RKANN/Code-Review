from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.db.mongodb import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import UserInDB
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db = Depends(get_db)):
    # Email kontrolü
    user = await db["users"].find_one({"email": user_in.email})
    if user:
        raise HTTPException(
            status_code=400,
            detail="Bu email adresine sahip bir kullanıcı zaten mevcut.",
        )
    
    user_dict = user_in.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    
    new_user = UserInDB(**user_dict)
    # Veritabanına kaydet
    result = await db["users"].insert_one(new_user.model_dump(by_alias=True, exclude={"id"}))
    
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    created_user["id"] = str(created_user.pop("_id"))
    return created_user

@router.post("/login", response_model=Token)
async def login(db = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
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
async def read_user_me(current_user: UserInDB = Depends(get_current_user)):
    user_dict = current_user.model_dump()
    user_dict["id"] = str(user_dict.pop("id", current_user.id))
    return user_dict
