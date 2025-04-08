from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import  get_db

### note the below is to import app from the main file which cant be done directly 
### so we import APIRouter
router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)



#### retrieve all posts
@router.get('/', response_model=List[schemas.Post])  
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    ### WITH DB -> send 200 on retrieve
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}
    '''

    ## with sqlalchemy
      ### make a test query
    posts = db.query(models.Post).all() ### printing posts with .all() will printteh underlying sql query
    return posts

##### retrieve A specific post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session=Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    ### foll is python code with summy db as array
    '''
    ### WITH normal python with array as DB
    print(id)
    retrieved_post = find_post(id)
    if not retrieved_post:
        
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id {id} was not found :("}
        
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} was not found :(" )
    return {"post_detail": f"Here is the post: {retrieved_post}"}
    '''

    '''
    ### WITH DB AND SQL -> send 200 on retrieve
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    retrieved_post = cursor.fetchone()
    if not retrieved_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} was not found." )
    return {"post_detail": retrieved_post}
    '''
    post = db.query(models.Post).filter(models.Post.id == id).first() ## first finds the first instance only and not all like all()
    #print(post)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
    return post

        

    

#############################################
############# POST Methods ###################
#############################################


### to create a post
@router.post('/', status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): ## the last dependencey weillrequire teh user to be authenticated
    ### posts has: title (str), content (str) (mandatory)
    #print(post)
    #print(post.model_dump())
    ## '''' foll is python code with example database in an array''
    '''
    post_dict = post.model_dump()
    id = randrange(0, 1000000)
    my_posts[id] = post_dict
    return {"data": post_dict}
    '''

    '''
    ### WITH DB -> send 201 on create
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
    '''

    #print(current_user.id)
    # the below method is time consuming since if theerare 50 fields in post well have to do a lotta work
    #new_post = models.Post(title=post.title, content=post.content, published=post.published) ## create a new post
    ## so we use the foll, we convert the post to dict and then unpack it using **
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    ### now commit
    db.add(new_post) ## add to db
    db.commit()  ## commit new post to db
    db.refresh(new_post)  ## just like returning
    return new_post




#############################################
############# PUT/PATCH Methods #############
#############################################

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    post_exists = find_post(id)
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} does not exist!")
    my_posts[id] = post.model_dump()
    return {"message": f"post with id {id} updated successfully!", "updated_post" : my_posts[id] }
    '''

    '''
    ### WITH DB -> send 200 on update
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} does not exist!")
    return {"message": f"post with id {id} updated successfully!", "updated_post" :  updated_post}
    '''

    post_query = db.query(models.Post).filter(models.Post.id == id)
    retrieved_post = post_query.first()
    if retrieved_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found!')
    if retrieved_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the requested action!")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

#############################################
############# DELETE Methods ###################
#############################################

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    output = delete(id)
    if not output:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} was not found :(. Delete Failed")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    '''

    '''
    #### WITH DB --> SEND 204 on delete
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found!')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    '''

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found!')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the requested action!")
    post_query.delete(synchronize_session=False) ## does not change session after delete and deleted rows are still available in session. this leads to inconsistencies
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)