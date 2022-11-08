from django.template import Library

register = Library()


@register.filter(name="split")
def split(value, key):
    value = value if value is not None else ''
    """
    Returns the value turned into a list.
    """
    return value.split(key)