# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# import hashlib
# SECRET_KEY = "your-secret-key"  # Change this to a secure secret!
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     sha256_password = hashlib.sha256(password.encode()).hexdigest()
#     return pwd_context.hash(sha256_password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     sha256_password = hashlib.sha256(plain_password.encode()).hexdigest()
#     return pwd_context.verify(sha256_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def decode_access_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload if "sub" in payload else None
#     except JWTError:
#         return None
