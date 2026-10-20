import asyncio
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.user import User
from backend.models.lab import Lab
from backend.models.equipment import Equipment
from backend.models.reservation import Reservation
from backend.common.exceptions import BusinessException
from backend.schemas.reservation import ReservationCreateRequest,ReservationResponse
from backend.common.response import PageResponse

def get_reservation_page_list(
    db: Session,
    current_user: User,
    page: int,
    page_size: int,
    status: int=None,
):
    """获取预约分页列表"""
    query=db.query(Reservation)
    if current_user.role!="admin":
        query=query.filter(Reservation.user_id==current_user.id)
    if status is not None:
        query=query.filter(Reservation.status==status)
    total=query.count()
    items=(
        query.order_by(
        Reservation.id.desc())
        .offset((page-1)*page_size)
        .limit(page_size)
        .all()
        )
    result=[]
    for item in items:
        res=ReservationResponse.model_validate(item)
        res.user_name=item.user.name if item.user else None
        res.lab_name=item.lab.name if item.lab else None
        res.equipment_name=item.equipment.name if item.equipment else None
        res.type="设备" if item.equipment else "实验室"
        result.append(res)
    return PageResponse(
        total=total,
        list=result
    )

        


def create_reservation(db: Session, current_user: User, data: ReservationCreateRequest):
    now=datetime.now()
    current_date=now.strftime("%Y-%m-%d")
    current_time=now.strftime("%H:%M:%S")
    if data.date < current_date:
        raise BusinessException(code=400, msg="预约日期不能早于当前日期")
    if data.end_time < data.start_time:
        raise BusinessException(code=400, msg="预约结束时间不能早于开始时间")
    if data.date==current_date and data.start_time < current_time:
        raise BusinessException(code=400, msg="预约开始时间不能早于当前时间")
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

def cancel_reservation(db: Session,current_user: User, id: int):
    """取消预约"""
    reservation=db.query(Reservation).filter(Reservation.id == id).first ()
    if not reservation:
        raise BusinessException(code=404, msg="预约不存在")
    if reservation.user_id!=current_user.id:
        raise BusinessException(code=403, msg="您没有权限取消该预约")
    if reservation.status!=0:
        raise BusinessException(code=400, msg="当前预约状态不能取消")
    reservation.status=3
    db.commit()

def audit_reservation(db: Session, id: int, status: int):
    """审核预约"""
    if status not in [1,2]:
        raise BusinessException(code=400, msg="审核状态错误")
    item=db.query(Reservation).filter(Reservation.id == id).first ()
    if not item:
        raise BusinessException(code=404, msg="预约不存在")
    if item.status!=0:
        raise BusinessException(code=400, msg="当前预约状态不能审核")
    item.status=status
    db.commit()

def expire_pending_reservation():
    """批量删除过期预约"""
    db=SessionLocal()
    try:
        now=datetime.now()
        today=now.strftime("%Y-%m-%d")
        time=now.strftime("%H:%M:%S")
        items=db.query(Reservation).filter(Reservation.status==0).all()
        changed=False
        for item in items:
            if item.date<today or (item.date==today and item.end_time<=time):
                item.status=3
                changed=True
        if changed: 
                db.commit()
    finally:
        db.commit()

async def run_expire_scan():
    """一分钟扫描执行业务"""
    while True:
        print("开始扫描过期预约")
        expire_pending_reservation()
        await asyncio.sleep(60)
    
