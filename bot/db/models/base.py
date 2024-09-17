import enum
from itertools import islice
from typing import ClassVar

import sqlalchemy as sa
from sqlalchemy import Column, MetaData, event
from sqlalchemy.orm import DeclarativeBase, declared_attr

from bot.utils.string_utils import pascal_to_snake, pluralize


@event.listens_for(sa.Enum, "before_parent_attach")
def process_enum_before_parent_attach(target: sa.Enum, _parent: Column) -> None:
    if target.name == "DEFAULT":
        target.name = pascal_to_snake(target.enum_class.__name__)


class ModelBase(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(table_name)s_%(column_0_N_name)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
    )
    type_annotation_map: ClassVar[dict] = {
        enum.Enum: sa.Enum(enum.Enum, name="DEFAULT"),
    }

    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        model_name = pascal_to_snake(cls.__name__.removesuffix("Model"))
        name_parts = model_name.split("_")
        name_parts[-1] = pluralize(name_parts[-1])
        return "_".join(name_parts)

    __repr_limit__: int | None = None
    __repr_ignore__: tuple[str, ...] = ()

    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)!r}"
            for col in islice(self.__table__.columns.keys(), self.__repr_limit__)
            if col not in self.__repr_ignore__
        ]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"
