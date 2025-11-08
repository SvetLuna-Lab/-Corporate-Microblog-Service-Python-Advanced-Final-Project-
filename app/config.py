# app/config.py

import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    DB_USER = os.environ.get("POSTGRES_USER", "microblog")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "microblog")
    DB_HOST = os.environ.get("POSTGRES_HOST", "db")
    DB_NAME = os.environ.get("POSTGRES_DB", "microblog")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", str(BASE_DIR / "uploads")
    )
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # max 5 MB per file
