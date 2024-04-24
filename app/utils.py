# force bcrypt==4.0.1 to keep working for this
# or use another library for hashing, better
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', dbname='fastapi',
#                                 user='postgres', password='postgres', cursor_factory=RealDictCursor)
#         cur = conn.cursor()
#         break
#     except Exception as e:
#         print(e)
#         time.sleep(2)
