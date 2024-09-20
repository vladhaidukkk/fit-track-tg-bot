from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.core import inject_session
from bot.db.models import UserModel
from bot.errors import UserAlreadyExistsError, UserNotFoundError


@inject_session
async def add_user(session: AsyncSession, *, id_: int, username: str | None = None) -> UserModel:
    try:
        new_user = UserModel(id=id_, username=username)
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


@inject_session
async def update_user(session: AsyncSession, *, id_: int, username: str | None = None) -> UserModel:
    user_query = select(UserModel).filter_by(id=id_)
    user = await session.scalar(user_query)
    if not user:
        raise UserNotFoundError(id_=id_)

    user.username = username
    await session.commit()
    return user
