from django import template

register = template.Library()


@register.simple_tag
def get_attendance_check(obj, get_check, *args):
    method = getattr(obj, get_check)
    return method(*args)


@register.simple_tag
def get_attendance_num(obj, get_num, *args):
    method = getattr(obj, get_num)
    return method(*args)
