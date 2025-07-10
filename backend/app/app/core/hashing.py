from passlib.context import CryptContext

pc=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
        return pc.hash(password)

def verify_password(plain_password:str, hash_password:str):
        return pc.verify(plain_password, hash_password)
    
