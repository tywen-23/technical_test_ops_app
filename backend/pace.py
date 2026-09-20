from calendar import monthrange
from datetime import date, datetime, timedelta, timezone


MALAYSIA_TIMEZONE = timezone(timedelta(hours=8))


def malaysia_today():
    return datetime.now(MALAYSIA_TIMEZONE).date()


def calculate_pace(month, mtd_revenue, target, today=None):
    """Calculate pace-to-target metrics for one selected month."""
    if not month:
        return None

    today = today or malaysia_today()
    month_start = date.fromisoformat(f"{month}-01")
    days_in_month = monthrange(month_start.year, month_start.month)[1]

    selected_month = (month_start.year, month_start.month)
    current_month = (today.year, today.month)

    revenue = round(float(mtd_revenue or 0), 2)
    target_value = float(target) if target is not None else None

    if selected_month < current_month:
        elapsed_days = days_in_month
        projected_revenue = revenue
    elif selected_month == current_month:
        elapsed_days = today.day
        projected_revenue = revenue / elapsed_days * days_in_month
    else:
        elapsed_days = 0
        projected_revenue = None

    if (
        projected_revenue is not None
        and target_value is not None
        and target_value > 0
    ):
        variance_amount = projected_revenue - target_value
        variance_pct = variance_amount / target_value * 100
        status = "on_track" if variance_amount >= 0 else "at_risk"
    else:
        variance_amount = None
        variance_pct = None
        status = "n/a"

    if (
        selected_month == current_month
        and target_value is not None
        and target_value > 0
    ):
        remaining_to_target = max(target_value - revenue, 0)
        remaining_days = days_in_month - elapsed_days

        if remaining_to_target == 0:
            required_daily_revenue = 0.0
        elif remaining_days > 0:
            required_daily_revenue = remaining_to_target / remaining_days
        else:
            required_daily_revenue = None
    else:
        remaining_to_target = None
        remaining_days = None
        required_daily_revenue = None

    return {
        "mtd_revenue": revenue,
        "elapsed_days": elapsed_days,
        "days_in_month": days_in_month,
        "projected_revenue": (
            round(projected_revenue, 2)
            if projected_revenue is not None
            else None
        ),
        "target": target_value,
        "variance_amount": (
            round(variance_amount, 2)
            if variance_amount is not None
            else None
        ),
        "variance_pct": (
            round(variance_pct, 1)
            if variance_pct is not None
            else None
        ),
         "remaining_to_target": (
            round(remaining_to_target, 2)
            if remaining_to_target is not None
            else None
        ),
        "remaining_days": remaining_days,
        "required_daily_revenue": (
            round(required_daily_revenue, 2)
            if required_daily_revenue is not None
            else None
        ),
        "status": status,
    }