from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import UserModel
from bot.errors import UserAlreadyExistsError


@inject_session
async def add_user(session: AsyncSession, *, id_: int) -> UserModel:
    try:
        new_user = UserModel(id=id_)
        session.add(new_user)
        await session.commit()
    except IntegrityError as error:
        raise UserAlreadyExistsError(id_=id_) from error
    else:
        return new_user


@inject_session
async def get_user(session: AsyncSession, *, id_: int) -> UserModel | None:
    query = select(UserModel).filter_by(id=id_)
    return await session.scalar(query)
