from getpass import getpass
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    password = getpass("Введите пароль: ")
    hashed = hash_password(password)
    print("Argon2 хеш:")
    print(hashed)
