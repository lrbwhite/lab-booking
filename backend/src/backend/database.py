from datetime import datetime

from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

from backend.config import config

engine = create_engine(config.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(declarative_base()):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="主键id")
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")