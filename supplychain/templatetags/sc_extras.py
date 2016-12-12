from django import template

register = template.Library()

@register.simple_tag
def model_get_field(obj, field):
    try:
        return getattr(obj, field)
    except:
        return "Foreignkey missing!"
