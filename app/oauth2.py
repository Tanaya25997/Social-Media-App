from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import exceptions as jwt_exceptions
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from sqlalchemy.orm import Session



## This is telling FastAPI that for any secured endpoint, it expects a Bearer token in the header
## 👉 The token will be generated from /login endpoint.
## 👉 The user will login → API will generate JWT → User uses JWT for future requests.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

# SECRET_KEY --> the key which api will send with which we can sign the signature [Header(contains algo and metadata) + Payload (some user data) + Secret]
# ALGORITHM 
# Expiration time ---> to expire login 


## this is some really lomg random string 
# to get a string like this run:
# openssl rand -hex 32
SECRETE_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc)  + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):

    try: 
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])

        id =  str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    
    except jwt_exceptions.PyJWTError:
        raise credentials_exception
    
    return token_data


### the Depends(oauth2_scheme) Automatically extracts the token from: Authorization: Bearer <token>
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()


    return user