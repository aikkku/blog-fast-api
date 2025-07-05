from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, database, models


router = APIRouter()


#POST
@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create(request:schemas.Blog, db:Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id =1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#GET
@router.get('/blog', response_model=List[schemas.ShowBlog], tags=["Blog"])
def all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs 

@router.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=["Blog"])
def show(id:int, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not avilable")
    return blog 

#DELETE
@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
def destroy(id:int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'done'}

#PUT
@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blog"])
def update(id:int, request: schemas.Blog, db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request, synchronize_session=False)
    db.commit()
    return db.query(models.Blog).filter(models.Blog.id == id).first()


