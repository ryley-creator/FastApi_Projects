from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

db_url = 'mysql+pymysql://root:12341234@127.0.0.1:3306/expense_tracker'
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    



