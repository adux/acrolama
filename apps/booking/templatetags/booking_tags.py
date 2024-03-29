from django import template
from django.utils.html import escape
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def get_attendance_check(obj, get_check, *args):
    method = getattr(obj, get_check)
    return method(*args)


@register.simple_tag
def get_attendance_num(obj, get_num, *args):
    method = getattr(obj, get_num)
    return method(*args)


@register.simple_tag(takes_context=True)
def pass_get_filter(context):
    request = context['request']
    get_elements = request.GET.items()
    url_filter_string = ''
    for key, value in get_elements:
        if key != 'page':  # same if index == 0:
            url_filter_string += '&' + str(key) + '=' + str(value)

    return escape(url_filter_string)


@register.filter(name='addclass')
def addclass(value, arg):
    if value == "":
        return
    return value.as_widget(attrs={'class': arg})


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter(is_safe=True)
@stringfilter
def truncatechars_middle(value, arg):
    try:
        ln = int(arg)
    except ValueError:
        return value
    if len(value) <= ln:
        return value
    else:
        return '{}...{}'.format(value[:ln//2], value[-((ln+1)//2):])
