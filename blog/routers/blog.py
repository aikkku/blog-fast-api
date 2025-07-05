from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, database
from ..repository import blog


router = APIRouter(
    tags=['Blogs'],
    prefix="/blog"
)


#POST
@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db:Session = Depends(database.get_db)):
    return blog.create(request, db)

#GET
@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    return blog.all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id:int, response: Response, db: Session = Depends(database.get_db)):
    return blog.show(id, response, db)

#DELETE
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(database.get_db)):
    return blog.destroy(id, db)

#PUT
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Blog, db:Session = Depends(database.get_db)):
    return blog.update(id, request, db)


