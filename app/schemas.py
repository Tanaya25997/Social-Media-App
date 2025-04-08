from pydantic import BaseModel, EmailStr 
from datetime import datetime
from typing import Optional


### foll is our table schema inherining BaseModel from Pydantic - to verify our request
### pydantic model/schema model defines teh structure of a request and response
### it checks types a well as if what is mandatory is in teh reqiest or not 
### helps teh server deciced what it wants from teh client instead of giving the client full control over sending anything 


#### for posts table ###
### foll is the schema for request
class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True

class PostCreate(PostBase):
    pass


## foll is the schema for response.This helps us define what all things should be sent back to the user
# ### example: fields like id or any senstive info could be not sent!  
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int ## note: we dont add it to POstBase or PostCreate since well retrive the owener id from token instead of asking the user to send 
    class Config:
        from_attributes = True ### this is so that the output is converted to dict irrespective of what sqlalchemy obj it is 


#### for users table ###########

class UserCreate(BaseModel):
    email: EmailStr ### to verify that email is valid 
    password: str 

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True



# User Login 
class UserLogin(BaseModel):
    email: EmailStr 
    password: str

##### schema for token 


#token schema
class Token(BaseModel):
    access_token: str
    token_type: str 

# payload schema or data schema
class TokenData(BaseModel):
    id: Optional[str] = None