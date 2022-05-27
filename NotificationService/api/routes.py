from fastapi import APIRouter
from .endpoints import notification

router = APIRouter()
router.include_router(
    notification.router, prefix="/notification", tags=["Notifications"]
)
