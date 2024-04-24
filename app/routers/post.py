from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from . import oauth2
from typing import Optional, List


router = APIRouter(
    prefix="/posts",
    tags=[
        'Posts'
    ]
)


# /posts?limit=INT&skip=INT&search=STR
@router.get("/",  status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 2, skip: int = 0, search: Optional[str] = ""):

    results = []
    fetches = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id ==
                                                                                         models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    for post, votes in fetches:
        results.append({
            "post": post,
            "vote_count": votes
        })

    return results


@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}',  status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # response: Response

    records = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id ==
                                                                                         models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} was not found")
    return {"post": records[0], "votes": records[1]}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    records = db.query(models.Post).filter(models.Post.id == id).first()

    if records == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} does not exist")

    if records.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")

    db.delete(records)
    db.commit()

    return None


@router.put('/{id}', response_model=schemas.Post, status_code=status.HTTP_200_OK)
def update_post(id: int, postReceived: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    records = db.query(models.Post).filter(models.Post.id == id)

    if records is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} does not exist")

    if records.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform this action")

    records.update(postReceived.__dict__)
    db.commit()

    # Fetch and return the updated post
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    return updated_post
