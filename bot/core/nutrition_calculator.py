from bot.enums import Gender


def calc_lbm(*, full_weight: float, fat_pct: int) -> float:
    """Calculate lean body mass (LBM).

    Args:
        full_weight: Full weight of the person in kilograms.
        fat_pct: Body fat percentage.

    Returns:
        The lean body mass in kilograms.

    """
    fat_weight = full_weight * fat_pct / 100
    return full_weight - fat_weight


def calc_bmr(*, gender: Gender, age: int, height: float, weight: float, fat_pct: int) -> float:
    """Calculate basal metabolic rate (BMR).

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.

    Returns:
        The BMR in calories/day.

    """
    lbm = calc_lbm(full_weight=weight, fat_pct=fat_pct)
    if gender == Gender.MALE:
        return 88.362 + (13.397 * lbm) + (4.799 * height) - (5.677 * age)
    assert gender == Gender.FEMALE, gender
    return 447.593 + (9.247 * lbm) + (3.098 * height) - (4.33 * age)


def calc_calories(*, gender: Gender, age: int, height: float, weight: float, fat_pct: int, amr: float) -> float:
    """Calculate daily calorie needs.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity Multiplier Rate (e.g., 1.2 for sedentary, 1.375 for lightly active, etc.).

    Returns:
        The daily calorie needs in calories/day.

    """
    bmr = calc_bmr(gender=gender, age=age, height=height, weight=weight, fat_pct=fat_pct)
    return bmr * amr * 1.1
