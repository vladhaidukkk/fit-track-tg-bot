from typing import TypedDict

from bot.core.enums import ActivityRate, BiologicalGender, WeightTarget


def calc_lbm(*, full_weight: float, fat_pct: float) -> float:
    """Calculate lean body mass (LBM).

    Args:
        full_weight: Full weight of the person in kilograms.
        fat_pct: Body fat percentage.

    Returns:
        The lean body mass in kilograms.

    """
    fat_weight = full_weight * fat_pct / 100
    return full_weight - fat_weight


def calc_bmr(*, gender: BiologicalGender, age: int, height: float, weight: float, fat_pct: float) -> float:
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
    return (
        88.362 + (13.397 * lbm) + (4.799 * height) - (5.677 * age)
        if gender == BiologicalGender.MALE
        else 447.593 + (9.247 * lbm) + (3.098 * height) - (4.33 * age)
    )


def calc_tef(
    gender: BiologicalGender, age: int, height: float, weight: float, fat_pct: float, amr: ActivityRate
) -> float:
    """Calculate the thermic effect of food (TEF).

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity multiplier rate (e.g., sedentary, lightly active, etc.).

    Returns:
        The TEF in calories/day.

    """
    bmr = calc_bmr(gender=gender, age=age, height=height, weight=weight, fat_pct=fat_pct)
    return bmr * amr.value / 10


def calc_calories(
    *,
    gender: BiologicalGender,
    age: int,
    height: float,
    weight: float,
    fat_pct: float,
    amr: ActivityRate,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> tuple[float, float]:
    """Calculate min and max daily calorie needs.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity multiplier rate (e.g., sedentary, lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        Min and max daily calorie needs in calories/day.

    """
    bmr = calc_bmr(gender=gender, age=age, height=height, weight=weight, fat_pct=fat_pct)
    tef = calc_tef(gender=gender, age=age, height=height, weight=weight, fat_pct=fat_pct, amr=amr)

    target_to_coefficients = {
        # Males: -10-15%, Females: -16-21%.
        WeightTarget.LOSE: (0.85, 0.9) if gender == BiologicalGender.MALE else (0.79, 0.84),
        WeightTarget.MAINTAIN: (1, 1),
        # Males: +10-15%, Females: +7-13%.
        WeightTarget.GAIN: (1.1, 1.15) if gender == BiologicalGender.MALE else (1.07, 1.13),
    }
    min_coefficient, max_coefficient = target_to_coefficients[target]

    daily_calories = (bmr * amr.value) + tef
    return daily_calories * min_coefficient, daily_calories * max_coefficient


def calc_proteins(*, weight: float, fat_pct: float, target: WeightTarget = WeightTarget.MAINTAIN) -> float:
    """Calculate daily protein needs.

    Args:
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        target: Desired impact on weight from a process perspective.

    Returns:
        The daily protein needs in grams/day.

    """
    lbm = calc_lbm(full_weight=weight, fat_pct=fat_pct)
    coefficient = 2.5 if target == WeightTarget.LOSE else 1.6
    return lbm * coefficient


def calc_fats(*, weight: float, fat_pct: float) -> float:
    """Calculate daily fat needs.

    Args:
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.

    Returns:
        The daily fat needs in grams/day.

    """
    return calc_lbm(full_weight=weight, fat_pct=fat_pct)


def calc_carbohydrates(
    *,
    gender: BiologicalGender,
    age: int,
    height: float,
    weight: float,
    fat_pct: float,
    amr: ActivityRate,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> tuple[float, float]:
    """Calculate min and max daily carbohydrate needs.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity multiplier rate (e.g., sedentary, lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        Min and max daily carbohydrate needs in grams/day.

    """
    min_calories, max_calories = calc_calories(
        gender=gender,
        age=age,
        height=height,
        weight=weight,
        fat_pct=fat_pct,
        amr=amr,
        target=target,
    )
    proteins = calc_proteins(weight=weight, fat_pct=fat_pct, target=target)
    fats = calc_fats(weight=weight, fat_pct=fat_pct)
    return (min_calories - (proteins * 4) - (fats * 9)) / 4, (max_calories - (proteins * 4) - (fats * 9)) / 4


def calc_water(*, weight: float, fat_pct: float) -> float:
    """Calculate daily water needs.

    Args:
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.

    Returns:
        The daily water needs in liters/day.

    """
    lbm = calc_lbm(full_weight=weight, fat_pct=fat_pct)
    return lbm / 20


def calc_fiber(
    *,
    gender: BiologicalGender,
    age: int,
    height: float,
    weight: float,
    fat_pct: float,
    amr: ActivityRate,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> tuple[float, float]:
    """Calculate min and max daily fiber needs.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity multiplier rate (e.g., sedentary, lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        Min and max daily fiber needs in grams/day.

    """
    min_calories, max_calories = calc_calories(
        gender=gender,
        age=age,
        height=height,
        weight=weight,
        fat_pct=fat_pct,
        amr=amr,
        target=target,
    )
    return min_calories / 1000 * 10, max_calories / 1000 * 10


def calc_sugar(
    *,
    gender: BiologicalGender,
    age: int,
    height: float,
    weight: float,
    fat_pct: float,
    amr: ActivityRate,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> tuple[float, float]:
    """Calculate norm and max daily sugar intake.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity multiplier rate (e.g., sedentary, lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        Norm and max daily sugar intake in grams/day.

    """
    min_calories, max_calories = calc_calories(
        gender=gender,
        age=age,
        height=height,
        weight=weight,
        fat_pct=fat_pct,
        amr=amr,
        target=target,
    )
    avg_calories = (min_calories + max_calories) / 2
    return avg_calories * 0.05 / 4, avg_calories * 0.1 / 4


def calc_salt(*, weight: float, fat_pct: float) -> float:
    """Calculate daily salt needs.

    Args:
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.

    Returns:
        The daily salt needs in grams/day.

    """
    lbm = calc_lbm(full_weight=weight, fat_pct=fat_pct)
    return lbm / 10


def calc_caffeine(*, weight: float) -> tuple[float, float]:
    """Calculate norm and max daily caffeine intake.

    Args:
        weight: Weight of the person in kilograms.

    Returns:
        Norm and max daily caffeine intake in milligrams/day.

    """
    return weight * 2.5, weight * 5


class NutritionalProfile(TypedDict):
    calories: tuple[float, float]
    proteins: float
    fats: float
    carbohydrates: tuple[float, float]
    water: float
    fiber: tuple[float, float]
    sugar: tuple[float, float]
    salt: float
    caffeine: tuple[float, float]


def calc_nutritional_profile(
    *,
    gender: BiologicalGender,
    age: int,
    height: float,
    weight: float,
    fat_pct: float,
    amr: ActivityRate,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> NutritionalProfile:
    """Calculate a comprehensive nutritional profile.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity multiplier rate (e.g., sedentary, lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        A dictionary containing the nutritional profile: min and max calories, proteins, fats,
        min and max carbohydrates, water, min and max fiber, salt, caffeine norm, and maximum caffeine.

    """
    return NutritionalProfile(
        calories=calc_calories(
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            fat_pct=fat_pct,
            amr=amr,
            target=target,
        ),
        proteins=calc_proteins(weight=weight, fat_pct=fat_pct, target=target),
        fats=calc_fats(weight=weight, fat_pct=fat_pct),
        carbohydrates=calc_carbohydrates(
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            fat_pct=fat_pct,
            amr=amr,
            target=target,
        ),
        water=calc_water(weight=weight, fat_pct=fat_pct),
        fiber=calc_fiber(
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            fat_pct=fat_pct,
            amr=amr,
            target=target,
        ),
        sugar=calc_sugar(
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            fat_pct=fat_pct,
            amr=amr,
            target=target,
        ),
        salt=calc_salt(weight=weight, fat_pct=fat_pct),
        caffeine=calc_caffeine(weight=weight),
    )
