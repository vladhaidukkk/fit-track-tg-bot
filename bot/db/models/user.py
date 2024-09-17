from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.model_types import created_at

from .base import ModelBase


class UserModel(ModelBase):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[created_at]
