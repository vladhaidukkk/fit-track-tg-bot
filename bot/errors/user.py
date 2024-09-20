from .base import CustomError


class UserAlreadyExistsError(CustomError):
    def __init__(self, id_: int) -> None:
        super().__init__(f"user with id={id_} already exists")


class UserNotFoundError(CustomError):
    def __init__(self, id_: int) -> None:
        super().__init__(f"user with id={id_} does not exist")
