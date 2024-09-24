def format_number(number: int | float, unit: str = "", *, sep: str = " ", precision: int = 2) -> str:
    formatted_number = f"{number:.{precision}f}".rstrip(".0") if isinstance(number, float) else f"{number}"
    return f"{formatted_number}{sep}{unit}" if unit else formatted_number


def format_age(age: int) -> str:
    if age % 10 == 1 and age % 100 != 11:
        word = "рік"
    elif 2 <= age % 10 <= 4 and not (12 <= age % 100 <= 14):
        word = "роки"
    else:
        word = "років"

    return f"{age} {word}"
