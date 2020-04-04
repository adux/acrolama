from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# NOTE: For custom names register through 'libraries' argument to DjandoTeamplte

# {{var|foo:"bar"}} bar is arg var is var in foo.

@register.filter
@stringfilter
def get_icon(cat):
    if cat == 'CY':
        icon = 'fas fa-cogs'
    elif cat == 'WS':
        icon = 'fas fa-cog'
    elif cat == 'MC':
        icon = 'fas fa-redo'
    elif cat == 'CA':
        icon = 'fas fa-star'
    elif cat == 'FT':
        icon = 'fas fa-rocket'
    elif cat == 'RT':
        icon = 'fas fa-seeding'
    else:
        icon = 'fas fa-snowflake'
        pass
    return icon
