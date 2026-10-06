import os

# Use the full DATABASE_URL provided by Vercel/Neon
SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")

# SQLAlchemy requires the URL to start with postgresql:// not postgres://
if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
