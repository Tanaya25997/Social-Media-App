from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from . import models
from .database import engine
from .routers import post,user, auth




##define teh cryptigraphic algo to be used
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_social_network', user='postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected to database!")
        break
    except Exception as e:
        print("Connection to database failed :(")
        print(f'Error = {e}')
        time.sleep(2)

#############################################
############# GET Methods ###################
#############################################

app.include_router(post.router) ## this includes the router from post.py
app.include_router(user.router) ## this includes the router from user.py
app.include_router(auth.router) ## this includes the router from auth.py


@app.get('/')
async def root():
    return {"Message" : "Hi"}


'''
Note: below was just a dummy way to store data in dict and test the paths
my_posts = {1 : {"title": "post 1", "content": "post 1 content"}, 2: {"title": "post 2", "content": "post 2 content"}}


def find_post(id):
    if id in my_posts:
        return my_posts[id]
    return False


def delete(id):
    if id in my_posts:
        del my_posts[id]
        return True 
    return False

##########################################################################################
############# Just a test route after adding sqlalchemy ###################
##########################################################################################
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)): ## the arg here asked get_db to get teh session

    ### make a test query
    posts = db.query(models.Post).all() ### printing posts with .all() will printteh underlying sql query
    return posts

'''







