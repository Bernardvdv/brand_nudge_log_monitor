from django import template

register = template.Library()


@register.filter
def check_month(value):
    if value is None:
        return 'Select or create period'
    return value
