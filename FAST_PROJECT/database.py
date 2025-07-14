from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_url = 'mysql+pymysql://root:12341234@127.0.0.1/fast_app'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()