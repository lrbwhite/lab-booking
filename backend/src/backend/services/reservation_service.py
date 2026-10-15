from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.lab import Lab
from backend.common.exceptions import BusinessException
from backend.schemas.reservation import ReservationCreateRequest

def create_reservation(db: Session, current_user: User, data: ReservationCreateRequest):
    if data.end_time < data.start_time:
        raise BusinessException(code=400, msg="预约时间不能早于开始时间")
    lab = db.query(Lab).filter(Lab.id == data.lab_id).first()
    if not lab:
        raise BusinessException(code=404, msg="实验室不存在")
    if lab.status!=1:
        raise BusinessException(code=400, msg="实验室已关闭")
    if lab.open_time and data.start_time < lab.open_time:
        raise BusinessException(code=400, msg="预约时间不能早于实验室开放时间")
    if lab.close_time and data.end_time > lab.close_time:
        raise BusinessException(code=400, msg="预约时间不能晚于实验室关闭时间")

    #equipment_id不为空，则表示这次是预约实验室设备
    if data.equipment_id:
        equipment=db.query(Equipment).filter(Equipment.id == data.equipment_id).first()
    if not equipment:
        raise BusinessException(code=404, msg="实验室设备不存在")
    if equipment.status!=1:
        raise BusinessException(code=400, msg="实验室设备正在维修")

    #实验室或设备是否是可预约状态
    query=db.query(Reservation).filter(
        Reservation.lab_id==data.lab_id,
        Reservation.date==data.date,
        Reservation.status.in_([0,1]),#0表示待审核，1表示已通过
        Reservation.start_time<=data.end_time,
        Reservation.end_time>=data.start_time
    )
    if data.equipment_id:
        query=query.filter(Reservation.equipment_id==data.equipment_id)#预约实验室设备
    else:
        query=query.filter(Reservation.equipment_id.is_(None))#预约实验室
    if query.first():
        raise BusinessException(code=400, msg="实验室或设备已被预约")

    reservation_model=Reservation(
        user_id=current_user.id,
        lab_id=data.lab_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        equipment_id=data.equipment_id,
        status=0,
    )

    db.add(reservation_model)
    db.commit()







    
