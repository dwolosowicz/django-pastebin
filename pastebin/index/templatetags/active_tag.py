from django import template
from django.core.urlresolvers import resolve


register = template.Library()


@register.simple_tag
def add_active(request, *names):
    """ Return the string 'active' current request.path is same as name

    Aruguments:
        request  -- Django request object
        *names   -- names of the matching urls
    """

    current_url_name = resolve(request.path).url_name

    if any(current_url_name == name for name in names):
        return 'active'

    return ''
