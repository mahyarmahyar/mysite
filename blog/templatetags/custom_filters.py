from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='truncatewords_custom')
@stringfilter
def truncatewords_custom(value, arg):
    """
    Truncates a string after a certain number of words.
    Argument: Number of words to truncate after.
    """
    words = value.split()
    if len(words) > arg:
        value = ' '.join(words[:arg]) + ' ...'
    return value
