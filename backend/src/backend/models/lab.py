from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column
from backend.database import Base

class Lab(Base):
    __tablename__ = "labs"
    __table_args__ = {"comment":"实验室"}

    name: Mapped[str] = mapped_column(String(50), comment="名称")
    description: Mapped[str] = mapped_column(String(255), comment="简介",nullable=False)
    location: Mapped[str] = mapped_column(String(100), comment="位置",nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, comment="容量",default=0)
    open_time: Mapped[str] = mapped_column(String(20), comment="开放开始时间",nullable=False)
    close_time: Mapped[str] = mapped_column(String(20), comment="开放结束时间",nullable=False)
    status: Mapped[int] = mapped_column(Integer, comment="状态,1:开放,0:关闭",default=1)


