from aiogram import Router

from .calc_cpfc import router as calc_cpfc_router
from .calc_food_allocation import router as calc_food_allocation_router
from .calc_pfc import router as calc_pfc_router
from .leave_feedback import router as leave_feedback_router

router = Router(name=__name__)
router.include_routers(
    calc_cpfc_router,
    calc_pfc_router,
    calc_food_allocation_router,
    leave_feedback_router,
)
