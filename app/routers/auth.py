from fastapi import APIRouter, Depends, status, HTTPException, Response 
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm ## with this instead of passing user credsin teh body we pass it in a utility providedby fatapi 
from .. import database, schemas, models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    ### the OAuth2PasswordRequestForm returns two fields as follows note: in dict format
    ### username = "xxxx"
    ### password = "xxxx"
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")  ## dont be specific to avoid guess work
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create a token 
    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    # return token 
    return {"access_token": access_token, "token_type": "bearer"}