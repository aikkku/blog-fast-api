from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        hashedPassword = pwd_context.hash(password)
        return hashedPassword
    
    def verify(hashed:str, password: str):
        return pwd_context.verify(password, hashed)