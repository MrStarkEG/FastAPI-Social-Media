from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from . import oauth2


router = APIRouter(
    prefix="/vote",
    tags=[
        'Vote'
    ]
)


@router.post("/",)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="there is no such post")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user)
    found_vote = vote_query.first()

    # Add a vote
    if vote.dir == 1:

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="you can't vote on the same post twice")

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    # Remove a vote
    if vote.dir == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="you can't remove a vote you didn't make")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

    # making sure the user inserts only vote.dir=0|1
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="dir can only be 1 | 0")
