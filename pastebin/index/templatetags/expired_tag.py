from django import template
from django.contrib.humanize.templatetags.humanize import naturaltime


register = template.Library()


def _expired_text(paste):
    if paste.expired():
        return "expired"

    return "expires in"


@register.simple_tag
def expired(paste):
    """ Returns the right form for expired field in pastes

    Keyword aruguments:
        paste -- Paste object
    """
    text = _expired_text(paste)
    humanized_time = naturaltime(paste.expires())

    return "{} {}".format(text, humanized_time.encode('utf-8'))
