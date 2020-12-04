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


def get_weekday_dates_for_period(startdate, enddate, weekday):
    """
    @param startdate date obj
    @param enddate date obj
    @param weekday int 0 Monday till 6 Sunday
    @return a list of dates
    """
    import datetime

    dates = []
    delta = enddate - startdate + datetime.timedelta(days=1)

    for x in range(delta.days):
        checkdate = startdate + datetime.timedelta(days=x)
        if checkdate.weekday() == weekday:
            dates.append(checkdate)

    return dates
