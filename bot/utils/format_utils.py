def format_number(number: int | float, unit: str = "", *, sep: str = " ", precision: int = 1) -> str:
    formatted_number = f"{number:.0f}" if number.is_integer() else f"{number:.{precision}f}".rstrip("0").rstrip(".")
    return f"{formatted_number}{sep}{unit}" if unit else formatted_number


def format_numbers_range(
    start_number: int | float, end_num: int | float, unit: str = "", *, sep: str = " ", precision: int = 1
) -> str:
    formatted_start_number = format_number(start_number, precision=precision)
    formatted_end_number = format_number(end_num, precision=precision)

    if formatted_start_number == formatted_end_number:
        return formatted_start_number

    return (
        f"{formatted_start_number}-{formatted_end_number}{sep}{unit}"
        if unit
        else f"{formatted_start_number}-{formatted_end_number}"
    )


def format_age(age: int) -> str:
    if age % 10 == 1 and age % 100 != 11:
        word = "рік"
    elif 2 <= age % 10 <= 4 and not (12 <= age % 100 <= 14):
        word = "роки"
    else:
        word = "років"

    return f"{age} {word}"
