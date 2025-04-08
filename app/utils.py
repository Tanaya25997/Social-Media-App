from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password:str):
    #### hash the password from user.password
    ### note: hasing is a one way street
    return pwd_context.hash(password)

def verify(plain_password, hased_password):
    return pwd_context.verify(plain_password, hased_password)