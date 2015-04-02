from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
 
register = template.Library()

@register.simple_tag
def is_author(request, user):
    """ Return True for Pastes which have been created by User with username
    
    Keyword aruguments:
    request  -- Django request object
    user -- user object
    """

    return request.user.id == user.id