from django.utils.http import urlencode
from django.urls import reverse


# Tests for the UserPassesTestMixin
def staff_check(user):
    return user.is_staff


def teacher_check(user):
    return user.is_teacher


def herd_check(user):
    try:
        if user.is_teacher or user.is_staff:
            return True
    except AttributeError:
        return False


def build_url(*args, **kwargs):
    """
    args has de url name for reverse
    pk needs to be a mapping aka dict
    """
    get = kwargs.pop("get", {})
    pk = kwargs.pop("pk", {})
    url = reverse(*args, kwargs=pk)
    if get:
        url += "?" + urlencode(get)
    return url
