from jose import JWTError, jwt
from copy import deepcopy
from datetime import datetime, timedelta
from .. import schemas, models
from ..database import get_db
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# EXP_time

SECRET_KEY = settings.database_password
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time


def create_access_token(data: dict):
    to_be_encoded = deepcopy(data)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_be_encoded.update({"exp": expire})

    encoded = jwt.encode(to_be_encoded, SECRET_KEY, algorithm=ALGORITHM)

    return encoded


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = str(payload.get("user_id"))

        if user_id is None:
            raise credentials_exception

        # Create a Token instance with the decoded user_id
        token_data = schemas.Token(
            access_token=token, token_type="bearer", id=user_id)

    except JWTError:
        raise credentials_exception

    return [token_data, user_id]


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    tokenData = verify_access_token(token, credential_exception)

    user_id = db.query(models.User).filter(
        models.User.id == tokenData[1]).first().id

    return user_id
