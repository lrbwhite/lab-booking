from fastapi import APIRouter,Depends
from backend.schemas.reservation import ReservationCreateRequest
from backend.services import reservation_service
from backend.dependencies.auth import get_current_user
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.common.response import Response

router=APIRouter(prefix="/reservation",tags=["预约相关接口"])

@router.post("")
def create_reservation(
    data: ReservationCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reservation_service.create_reservation(db, current_user, data)
    return Response.success()
