from django.utils.http import urlencode
from django.urls import reverse


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    pk = kwargs.pop('pk', {})
    url = reverse(*args, kwargs=pk)
    if get:
        url += '?' + urlencode(get)
    return url
