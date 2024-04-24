from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter, exceptions
from sqlalchemy import exc
from sqlalchemy.orm import Session
from ..database import get_db
from . import oauth2

router = APIRouter(
    prefix="/users",
    tags=[
        'Users'
    ]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=list[schemas.UserOut])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashing password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    # commiting changes
    try:
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return [new_user]
    except exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This email is already signed up")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    records = db.query(models.User).all()
    return records


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    records = db.query(models.User).filter(models.User.id == id)

    if not records:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="user does not exist")

    return records
