from django import template

register =template.Library()

@register.filter
def modulo(num, val):
    return num % val == 1

@register.filter
def modulo2(num, val):
    return num % val == 2

@register.filter
def modulo3(num, val):
    return num % val == 0