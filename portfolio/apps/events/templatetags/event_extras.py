from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def pace(value: timedelta | None) -> str:
    """Format a pace duration as whole minutes and seconds."""
    if value is None:
        return ""

    total_seconds = round(value.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes}:{seconds:02d}"
