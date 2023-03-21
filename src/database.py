'''db connection related stuff'''

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import src.config as config

db_engine = create_engine(url=config.DB_CONNECTION_URL)
db_conn = db_engine.connect()
# db_conn.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()