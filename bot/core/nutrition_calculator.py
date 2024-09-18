from typing import TypedDict

from bot.enums import BiologicalGender, WeightTarget


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


def calc_bmr(*, gender: BiologicalGender, age: int, height: float, weight: float, fat_pct: int) -> float:
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


def calc_tef(gender: BiologicalGender, age: int, height: float, weight: float, fat_pct: int, amr: float) -> float:
    """Calculate the thermic effect of food (TEF).

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity Multiplier Rate (e.g., 1.2 for sedentary, 1.375 for lightly active, etc.).

    Returns:
        The TEF in calories/day.

    """
    bmr = calc_bmr(gender=gender, age=age, height=height, weight=weight, fat_pct=fat_pct)
    return bmr * amr / 10


def calc_calories(
    *,
    gender: BiologicalGender,
    age: int,
    height: float,
    weight: float,
    fat_pct: int,
    amr: float,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> float:
    """Calculate daily calorie needs.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity Multiplier Rate (e.g., 1.2 for sedentary, 1.375 for lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        The daily calorie needs in calories/day.

    """
    bmr = calc_bmr(gender=gender, age=age, height=height, weight=weight, fat_pct=fat_pct)
    tef = calc_tef(gender=gender, age=age, height=height, weight=weight, fat_pct=fat_pct, amr=amr)

    target_to_coefficient = {
        WeightTarget.LOSE: 0.9,
        WeightTarget.MAINTAIN: 1,
        WeightTarget.GAIN: 1.1,
    }
    coefficient = target_to_coefficient[target]

    return (bmr * amr + tef) * coefficient


def calc_proteins(*, weight: float, fat_pct: int, target: WeightTarget = WeightTarget.MAINTAIN) -> float:
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


def calc_fats(*, weight: float, fat_pct: int) -> float:
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
    fat_pct: int,
    amr: float,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> float:
    """Calculate daily carbohydrate needs.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity Multiplier Rate (e.g., 1.2 for sedentary, 1.375 for lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        The daily carbohydrate needs in grams/day.

    """
    calories = calc_calories(
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
    return (calories - (proteins * 4) + (fats * 9)) / 4


def calc_water(*, weight: float, fat_pct: int) -> float:
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
    fat_pct: int,
    amr: float,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> float:
    """Calculate daily fiber needs.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity Multiplier Rate (e.g., 1.2 for sedentary, 1.375 for lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        The daily fiber needs in grams/day.

    """
    calories = calc_calories(
        gender=gender,
        age=age,
        height=height,
        weight=weight,
        fat_pct=fat_pct,
        amr=amr,
        target=target,
    )
    return calories / 1000 * 10


def calc_salt(*, weight: float, fat_pct: int) -> float:
    """Calculate daily salt needs.

    Args:
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.

    Returns:
        The daily salt needs in grams/day.

    """
    lbm = calc_lbm(full_weight=weight, fat_pct=fat_pct)
    return lbm / 10


def calc_caffeine_norm(*, weight: float) -> float:
    """Calculate normal daily caffeine intake.

    Args:
        weight: Weight of the person in kilograms.

    Returns:
        The normal daily caffeine intake in milligrams/day.

    """
    return weight * 2.5


def calc_caffeine_max(*, weight: float) -> float:
    """Calculate maximum daily caffeine intake.

    Args:
        weight: Weight of the person in kilograms.

    Returns:
        The maximum daily caffeine intake in milligrams/day.

    """
    return weight * 5


class NutritionalProfile(TypedDict):
    calories: float
    proteins: float
    fats: float
    carbohydrates: float
    water: float
    fiber: float
    salt: float
    caffeine_norm: float
    caffeine_max: float


def calc_nutritional_profile(
    *,
    gender: BiologicalGender,
    age: int,
    height: float,
    weight: float,
    fat_pct: int,
    amr: float,
    target: WeightTarget = WeightTarget.MAINTAIN,
) -> NutritionalProfile:
    """Calculate a comprehensive nutritional profile.

    Args:
        gender: Gender of the person.
        age: Age of the person in years.
        height: Height of the person in centimeters.
        weight: Weight of the person in kilograms.
        fat_pct: Body fat percentage.
        amr: Activity Multiplier Rate (e.g., 1.2 for sedentary, 1.375 for lightly active, etc.).
        target: Desired impact on weight from a process perspective.

    Returns:
        A dictionary containing the nutritional profile: calories, proteins, fats, carbohydrates, water, fiber, salt,
        caffeine norm, and maximum caffeine.

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
        salt=calc_salt(weight=weight, fat_pct=fat_pct),
        caffeine_norm=calc_caffeine_norm(weight=weight),
        caffeine_max=calc_caffeine_max(weight=weight),
    )
