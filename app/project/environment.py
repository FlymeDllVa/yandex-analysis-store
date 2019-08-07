import os

SECRET_KEY = os.environ.get('SECRET_KEY') or "ya-test"
POSTGRES_USER = os.environ.get('POSTGRES_USER') or "postgres"
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') or "postgres"
POSTGRES_HOST = os.environ.get('POSTGRES_PASSWORD') or "localhost"
POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or 5432
POSTGRES_DB = os.environ.get('POSTGRES_DB') or "tests"
REDIS_HOST = os.environ.get("REDIS_HOST") or "localhost"
REDIS_PORT = os.environ.get("REDIS_PORT") or 6379
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD") or "redis"
REDIS_DB = os.environ.get("REDIS_DB") or 0
DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/"