from django import template

register = template.Library()

@register.simple_tag
def model_get_field(obj, field):
    return getattr(obj, field)
