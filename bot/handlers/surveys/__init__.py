from aiogram import Router

from .adjust_calories import router as adjust_calories_router
from .calc_calories import survey_router as calc_calories_router
from .calc_food_allocation import survey_router as calc_food_allocation_router
from .leave_suggestion import survey_router as leave_suggestion_router

router = Router(name=__name__)
router.include_routers(
    calc_calories_router,
    adjust_calories_router,
    calc_food_allocation_router,
    leave_suggestion_router,
)
