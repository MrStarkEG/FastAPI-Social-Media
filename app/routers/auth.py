from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils
from . import oauth2

router = APIRouter(
    prefix='/login',
    tags=[
        'Authentication'
    ]
)


@router.get('/', response_model=schemas.Token)  # username:password
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    records = db.query(models.User).filter(
        user_creds.username == models.User.email).first()

    if not records:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="wrong credentials")

    if not utils.verify_password(user_creds.password, records.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="wrong credentials")

    access_token = oauth2.create_access_token(data={"user_id": records.id})

    return {"access_token": access_token, "token_type": "Bearer"}
