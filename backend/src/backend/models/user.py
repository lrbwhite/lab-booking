from backend.database import Base
from sqlalchemy import String
from sqlalchemy.orm import mapped_column,Mapped

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"comment":"用户表"}
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True,comment="用户ID")
    username:Mapped[str]=mapped_column(String(20),unique=True,comment="账户")
    password:Mapped[str]=mapped_column(String(20),comment="密码")
    role:Mapped[str]=mapped_column(String(20),nullable=False,comment="角色：学生/管理员")
    name:Mapped[str]=mapped_column(String(20),nullable=False,comment="名称")
    email:Mapped[str]=mapped_column(String(20),nullable=False,comment="邮箱")
    phone:Mapped[str|None]=mapped_column(String(20),comment="手机号")
    avatar:Mapped[str|None]=mapped_column(String(20),comment="头像")
