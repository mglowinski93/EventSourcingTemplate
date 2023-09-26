import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    f"postgresql://"
    f"{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}"
    f"@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/"
    f"{os.environ['DATABASE_NAME']}"
)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=100,
)


@contextmanager
def get_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    try:
        yield session
        session.commit()
        session.flush()
    except Exception as err:
        session.rollback()
        raise err from err
    finally:
        session.close()
