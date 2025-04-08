from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, utils
from ..database import  get_db


### note the below is to import app from the main file which cant be done directly 
### so we import APIRouter
router = APIRouter(
    prefix = "/users", 
    tags = ['Users']
)


############### Users table ######


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):


    #### hash the password from user.password
    ### note: hasing is a one way street
    hashed_pwd = utils.hash(user.password)


    try:
        user.password = hashed_pwd
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback() ## rollback transcation to maintain the db
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with this email id already exists")

@router.get('/{id}', response_model = schemas.UserOut)
def get_user(id: int,  db: Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist!")
    
    return user