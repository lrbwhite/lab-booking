from fastapi import APIRouter,Depends
from backend.schemas.reservation import ReservationCreateRequest,AuditReservationRequest
from backend.services import reservation_service
from backend.dependencies.auth import get_current_user,get_current_admin
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.common.response import Response

router=APIRouter(prefix="/reservation",tags=["预约相关接口"])

@router.get("/list")
def get_reservation_page_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    page_size: int = 10,
    status: int=None,
):
    """获取预约列表"""
    res=reservation_service.get_reservation_page_list(
        db,
        current_user,
        page,
        page_size,
        status,
    )
    return Response.success(res)


@router.post("")
def create_reservation(
    data: ReservationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reservation_service.create_reservation(db, current_user, data)
    return Response.success()

@router.put("/{reservation_id}/cancel")
def cancel_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reservation_service.cancel_reservation(db, current_user, reservation_id)
    return Response.success()

@router.put("/{reservation_id}/audit")
def audit_reservation(
    reservation_id: int,
    data: AuditReservationRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    reservation_service.audit_reservation(db, reservation_id, data.status)
    return Response.success()