from django.views.decorators.cache import cache_page


class CacheMixin(object):
    cache_timeout = 60 * 15  # 900 seconds or 15  Min cache

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)
