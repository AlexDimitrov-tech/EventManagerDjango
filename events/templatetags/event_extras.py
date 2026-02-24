from django import template
from datetime import date

register = template.Library()


@register.filter
def format_price(value):
    try:
        f = float(value)
        return 'Free' if f == 0 else '${:.2f}'.format(f)
    except (ValueError, TypeError):
        return value


@register.filter
def days_until(event_date):
    try:
        today = date.today()
        delta = (event_date - today).days

        if delta < 0:
            return f'{abs(delta)} days ago'
        elif delta == 0:
            return 'Today!'
        else:
            return f'in {delta} days'
    except Exception:
        return ''


@register.filter
def short_desc(text, length=120):
    try:
        s = str(text)
        return s if len(s) <= length else s[:length] + '...'
    except Exception:
        return text


@register.filter
def venue_size(capacity):
    try:
        cap = int(capacity)
        if cap < 50:
            return 'Intimate'
        elif cap < 200:
            return 'Small'
        elif cap < 1000:
            return 'Medium'
        return 'Large'
    except (ValueError, TypeError):
        return 'Unknown'
