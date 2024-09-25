def calc_food_allocation(first_dry_mass: float, second_dry_mass: float, total_ready_mass: float) -> tuple[float, float]:
    total_dry_mass = first_dry_mass + second_dry_mass
    coefficient = total_ready_mass / total_dry_mass
    return first_dry_mass * coefficient, second_dry_mass * coefficient
