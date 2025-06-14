from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


@app.get('/blog')
def index(limit:int = 10, published:bool = True, sort: Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {"data":f'{limit} published blog list'}
    else:
        return {"data":f'{limit} unpublished blog list'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished data'}

@app.get('/blog/{id}')
def blog(id: int):
    #fetch blog with id=id
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id: int):
    #fetch comments of blog id=id
    return {'data': {'1', '2'}}



#POST
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = False

@app.post('/blog')
def create_blog(blog: Blog):
    return {'data':f'Blog is created with title: {blog.title}'}

