from passlib.context import CryptContext

# Set up bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes the password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the provided password matches the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    pwd = 'TEST'
    print('password: ', pwd)
    hashed = hash_password(pwd)
    print('hashed: ', hashed)
    print('verified?: ', verify_password(pwd, hashed))