from django import template
from datetime import date, datetime

register = template.Library()

@register.filter
def format_date(value):
    if isinstance(value, date):
        return value.strftime('%B %d, %Y')
    return value

@register.filter
def format_time(value):
    if hasattr(value, 'strftime'):
        return value.strftime('%I:%M %p')
    return value

@register.filter
def truncate_text(value, length=100):
    if len(value) > length:
        return value[:length] + '...'
    return value

@register.filter
def format_price(value):
    return f"${value:.2f}"

