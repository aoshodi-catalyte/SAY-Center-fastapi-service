from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database URL configuration
# (Using host, port, username, password, and database name from Step 1)

DATABASE_URL = "postgresql://postgres:root@localhost:5432/say-center"

# 2. Engine creation
engine = create_engine(DATABASE_URL, echo=True)

# 3. Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Declarative Base
Base = declarative_base()
