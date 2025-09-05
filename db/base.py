from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from utils.config import CONNECTION_STRING, app_path

Base = declarative_base()

# mssql
# engine = create_engine(
#     f"mssql+pyodbc:///?odbc_connect={CONNECTION_STRING}",
#     fast_executemany=True
# )

# sqllite
engine = create_engine(f"sqlite:///{app_path('database.db')}", echo=False)

SessionLocal = sessionmaker(bind=engine)

__all__ = ["Base", "engine", "SessionLocal"]
