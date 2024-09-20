from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at

from .base import ModelBase


class UserModel(ModelBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    # NOTE: A unique constraint here may cause a conflict if a user changes their username on Telegram and another user
    # selects it before the original user returns to the bot. However, the likelihood of this happening is very low.
    username: Mapped[str | None] = mapped_column(unique=True)
    created_at: Mapped[created_at]
