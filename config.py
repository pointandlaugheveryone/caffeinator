import os

DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://fallback_url")