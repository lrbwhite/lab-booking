from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import ForeignKey,String
from backend.database import Base
from backend.models.user import User
from backend.models.lab import Lab
from backend.models.equipment import Equipment

class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = {"comment": "预约表"}

    user_id:Mapped[int]=mapped_column(ForeignKey("user.id"),comment="预约人",nullable=False)
    lab_id:Mapped[int]=mapped_column(ForeignKey("labs.id"),comment="实验室",nullable=False)
    equipment_id:Mapped[int]=mapped_column(ForeignKey("equipments.id"),comment="设备",nullable=True)
    date:Mapped[str]=mapped_column(String(10),comment="预约日期",nullable=False)
    start_time:Mapped[str]=mapped_column(String(20),comment="开始时间",nullable=False)
    end_time:Mapped[str]=mapped_column(String(20),comment="结束时间",nullable=False)
    remark:Mapped[str | None]=mapped_column(String(255),comment="备注",nullable=True)
    status:Mapped[int]=mapped_column(default=0,comment="状态：0-待审核,1-已通过,2-已取消，3-已拒绝,")

    user:Mapped["User"]=relationship()
    lab:Mapped["Lab"]=relationship()
    equipment:Mapped["Equipment"]=relationship()

