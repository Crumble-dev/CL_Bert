# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))
print("AWS_DEFAULT_REGION:", os.getenv("AWS_DEFAULT_REGION"))
print("S3_BUCKET:", os.getenv("S3_BUCKET"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

console.log("Environment variables loaded successfully.")