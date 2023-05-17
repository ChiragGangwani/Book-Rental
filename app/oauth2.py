from datetime import datetime, timedelta
from jose import jwt,JWTError
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from . import schemas,models
from .database import get_db
from sqlalchemy.orm import Session


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire =datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credidentials_exception):

    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id=payload.get('user_id')

        if id is None:
            raise credidentials_exception
        token_data=id

    except JWTError:
        raise credidentials_exception
    return token_data
    
async def get_current_user(token =Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    id=verify_access_token(token=token,credidentials_exception=credentials_exception)
    user=db.query(models.User).filter(models.User.id==id).first()

    return user

