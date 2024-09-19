def format_age(age: int) -> str:
    if age % 10 == 1 and age % 100 != 11:
        word = "рік"
    elif 2 <= age % 10 <= 4 and not (12 <= age % 100 <= 14):
        word = "роки"
    else:
        word = "років"

    return f"{age} {word}"
