from .user import router as user_router
from .auth import router as auth_router
from fastapi import APIRouter
from .files import router as files_router
from .lab import router as lab_router
from .equipment import router as equipment_router
from .reservation import router as reservation_router



router = APIRouter(prefix="/api")
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(files_router)
router.include_router(lab_router)
router.include_router(equipment_router)
router.include_router(reservation_router)
