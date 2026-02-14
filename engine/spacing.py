from datetime import datetime

def check_spacing(previous_time_str, current_time_str, min_spacing_hours):
    """
    Returns True if spacing violation exists.
    """

    time_format = "%H:%M"

    previous_time = datetime.strptime(previous_time_str, time_format)
    current_time = datetime.strptime(current_time_str, time_format)

    hours_diff = abs((current_time - previous_time).total_seconds()) / 3600

    return hours_diff < min_spacing_hours
