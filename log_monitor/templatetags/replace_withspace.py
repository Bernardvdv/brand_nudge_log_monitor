from django import template

register = template.Library()


@register.filter
def replace_withspace(value):
    return value.replace("_", " ")
