from django import template
from datetime import date

register = template.Library()


@register.filter
def format_price(value):
    try:
        price_float = float(value)
        if price_float == 0:
            return 'Free'
        else:
            formatted = '${:.2f}'.format(price_float)
            return formatted
    except (ValueError, TypeError):
        return value


@register.filter
def days_until(event_date):
    try:
        today = date.today()
        if event_date < today:
            days_ago = (today - event_date).days
            return str(days_ago) + ' days ago'
        elif event_date == today:
            return 'Today!'
        else:
            days_left = (event_date - today).days
            return 'in ' + str(days_left) + ' days'
    except Exception:
        return ''


@register.filter
def short_desc(text, length=120):
    try:
        text_str = str(text)
        if len(text_str) <= length:
            return text_str
        else:
            truncated = text_str[:length]
            return truncated + '...'
    except Exception:
        return text


@register.filter
def venue_size(capacity):
    try:
        cap = int(capacity)
        if cap < 50:
            result = 'Intimate'
        elif cap < 200:
            result = 'Small'
        elif cap < 1000:
            result = 'Medium'
        else:
            result = 'Large'
        return result
    except (ValueError, TypeError):
        return 'Unknown'
