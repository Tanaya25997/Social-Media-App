from app.database import Base 
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, relationship
from sqlalchemy.sql.expression import text

### Create Table post which extends Base
### This is the sql alchemy model
### or basically the table in our db
#### used to define cols and to do CRUD operations
class Post(Base):
    #### specify name for the table
    __tablename__ = 'posts'

    #### specify columns 
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable= False)
    owner = relationship("User")


### another table to store user info
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),nullable=False)

    
