from django import template
register = template.Library()

@register.filter
def multiply(value, arg):
    sum = value * arg
    return format(sum, '.2f')