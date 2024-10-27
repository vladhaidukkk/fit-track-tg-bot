from aiogram import Router

from .actions import router as actions_router
from .commands import primary_router as primary_commands_router
from .commands import secondary_router as secondary_commands_router
from .surveys import router as surveys_router

router = Router(name=__name__)
router.include_routers(
    primary_commands_router,
    surveys_router,
    secondary_commands_router,
    actions_router,
)
