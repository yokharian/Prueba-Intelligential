"""create in-memory database"""
from os import getenv

from sqlalchemy import (
    create_engine,
)

from build_database import fully_build_database

IN_MEMORY_DATABASE = True if getenv("IN_MEMORY_DATABASE", False) == "True" else False
BUILD_DATABASE = getenv("BUILD_DATABASE", False)
DATE_FORMAT = "%d-%m-%Y"

DATABASE_PATH = "/db.sqlite3" if IN_MEMORY_DATABASE is False else ""
engine = create_engine("sqlite://" + DATABASE_PATH, echo=False)

if IN_MEMORY_DATABASE:
    fully_build_database(engine)
