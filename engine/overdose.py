def check_overdose(doses_today, max_daily_dose, single_dose_limit):
    """
    doses_today: list of numeric doses
    """

    total_dose = sum(doses_today)

    single_violation = any(d > single_dose_limit for d in doses_today)
    daily_violation = total_dose > max_daily_dose

    return single_violation or daily_violation, total_dose
