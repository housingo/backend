from fastapi import APIRouter
from .endpoints import payment

router = APIRouter()
router.include_router(payment.router, prefix="/payment", tags=["Payments"])
