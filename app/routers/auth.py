from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,util,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    tags=['Authentication']
)
@router.post("/login",response_model=schemas.Token)
async def login_user(user_credidentials:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credidentials.username).first()

    if not user or not util.verify(user_credidentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credidentials")

    access_token=oauth2.create_access_token(data={"user_id":user.id,"name":user.name})
    return {"access_token":access_token}
