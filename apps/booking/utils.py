from django.utils.http import urlencode
from django.urls import reverse


#  TODO: im not sure what kwargs.pop does. or if i can handle it differently
def build_url(*args, **kwargs):
    get = kwargs.pop("get", {})
    pk = kwargs.pop("pk", {})
    # TODO: this kwargs=pk doesn't look good, works, but i think its
    # super unelegant
    url = reverse(*args, kwargs=pk)
    if get:
        url += "?" + urlencode(get)
    return url
