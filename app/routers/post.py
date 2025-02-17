from .. import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
) 

# all posts using python ORM sqlalchemy
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0,
               search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts_query = db.query(models.Post,func.count(models.Vote.post_id,).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()     
    if not posts_query: return []
    posts = [ 
    schemas.PostOut(post=post, likes=likes)for post, likes in posts_query
    ]
    return posts 




# get user posts
@router.get("/user", response_model=List[schemas.Post])
def get_user_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts  
 
# create post using python ORM sqlalchemy
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) 
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post



# latest post Python ORM sqlalchemy
@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return  latest_post


# single post Python ORM sqlalchemy
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    posts_query = db.query(models.Post,func.count(models.Vote.post_id,).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not posts_query:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    post = schemas.PostOut(post=posts_query[0], likes=posts_query[1])
    return  post



# update post python sqlalchemy
@router.put("/{id}", response_model=schemas.Post) 
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    old_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not old_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if old_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    for key, value in post.model_dump().items():
        setattr(old_post, key, value)
    db.commit()
    db.refresh(old_post)
    return old_post


# delete post sqlalchemy
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)