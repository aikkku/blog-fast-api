from fastapi import FastAPI, Depends, Response, status, HTTPException
from . import schemas,models,hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#POST
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Blog"])
def create(request:schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id =1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#GET
@app.get('/blog', response_model=List[schemas.ShowBlog], tags=["Blog"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs 

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=["Blog"])
def show(id:int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not avilable")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with the id {id} is not available'}
    return blog 

#DELETE
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blog"])
def destroy(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'done'}

#PUT
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blog"])
def update(id:int, request: schemas.Blog, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request, synchronize_session=False)
    db.commit()
    return db.query(models.Blog).filter(models.Blog.id == id).first()


#USER


@app.post('/user', response_model=schemas.ShowUser, tags=["User"])
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=["User"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    return user
