from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import DeclarativeBase



SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi_social_network'

engine = create_engine(SQLALCHEMY_DATABASE_URL) ### engine established connection


class Base(DeclarativeBase):
    pass

## session talks to the db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


## dependency --> this gets a session to the db, performs the operation and then closes teh session
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()