import jdatetime
from django import template

register = template.Library()

@register.filter
def to_jalali(value, fmt='%Y/%m/%d'):
    if not value:
        return ''
    try:
        return jdatetime.datetime.fromgregorian(datetime=value).strftime(fmt)
    except Exception:
        return value 