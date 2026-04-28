from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.core.security import ALGORITHM
from app.schemas.user import TokenPayload
from app.db.mongodb import get_db
from app.models.user import UserInDB
from bson import ObjectId

bearer_scheme = HTTPBearer()

async def get_current_user(credentials = Depends(bearer_scheme), db = Depends(get_db)) -> UserInDB:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik bilgileri",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_dict = await db["users"].find_one({"_id": ObjectId(token_data.sub)})
    if user_dict is None:
        raise credentials_exception
        
    return UserInDB(**user_dict)
