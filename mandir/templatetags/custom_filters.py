from django import template

register = template.Library()


@register.simple_tag
def create_message(value, title, amt, date):
    return value.format(title, amt, date)