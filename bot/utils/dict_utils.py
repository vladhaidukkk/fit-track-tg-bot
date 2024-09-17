from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


def get_key_by_value(dict_: dict[K, V], target_value: V) -> K | None:
    return next((key for key, value in dict_.items() if value == target_value), None)
