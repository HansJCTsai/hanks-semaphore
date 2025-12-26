from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=True)


def verify_password(secretPassword: str, hashedPassword: str) -> bool:
    return pwd_context.verify(secret=secretPassword, hash=hashedPassword)


# hashed
def get_hashed_password(secretPassword: str) -> str:
    return pwd_context.hash(secret=secretPassword)
