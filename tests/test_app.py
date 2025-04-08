from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert  response.status_code == 200
    assert response.json() == {"Message" : "Hi"}  # Replace with actual response
'''
#Step 1: Create a new user for testing
def test_create_test_user():
    # Assuming you have a registration route in your app for creating users
    user_data = {
        "email": "abcde@gmail.com", 
        "password": "password"
    }
    response = client.post("/users", json=user_data)  # Assuming the registration route is "/register"
    
    assert response.status_code == 201, f"User creation failed: {response.text}"
    return user_data["email"]
'''

# Step 1: Get the authentication token
def get_token():
    login_data = {"username": "abcde@gmail.com", "password": "password"}
    response = client.post("/login", data=login_data)
    return response.json().get("access_token")

# Test GET posts endpoint with authentication
def test_get_posts():
    token = get_token()  # Step 2: Get the token
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/posts", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assuming it returns a list of posts



### integration test 
def test_create_user(client, setup_db):
    # Step 1: Create a user using the API endpoint
    user_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201

    # Step 2: Verify the user is in the database (using the `setup_db` fixture)
    db_user = setup_db.query(models.User).filter(models.User.email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.email == user_data["email"]


# Create a test client to interact with FastAPI
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client