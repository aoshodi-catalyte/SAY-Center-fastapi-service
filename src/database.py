"""SQLAlchemy database engine and session configuration.

Update ``DATABASE_URL`` to match your local PostgreSQL credentials, host, port,
and database name before running the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:root@localhost:5432/say-center"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
