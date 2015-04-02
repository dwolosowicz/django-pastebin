from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
 
register = template.Library()

def _determine_path(text, by_path):
    if by_path:
        return text
    else:
        return reverse(text)


@register.simple_tag
def add_active(request, name, by_path=False):
    """ Return the string 'active' current request.path is same as name
    
    Keyword aruguments:
    request  -- Django request object
    name     -- name of the url or the actual path
    by_path  -- True if name contains a url instead of url name

    Tag silences NoReverseMatch exception, 
    so it doesn't crash the website when the action doesn't exist.
    """

    try:
        path = _determine_path(name, by_path)
        
        if request.path == path:
            return 'active'
        else:
            return ''
    except NoReverseMatch:
        return ''
