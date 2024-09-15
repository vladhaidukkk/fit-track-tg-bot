from aiogram import Router

from .calc_calories import router as calc_calories_router

router = Router(name=__name__)
router.include_routers(calc_calories_router)
