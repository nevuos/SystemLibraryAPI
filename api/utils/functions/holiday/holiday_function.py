import holidays

br_holidays = holidays.Brazil()


def is_business_day(date) -> bool:
    return date.weekday() < 5 and date not in br_holidays
