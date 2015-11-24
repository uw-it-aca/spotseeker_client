from spotseeker_restclient.dao_implementation.live import get_con_pool, \
    get_live_url
from spotseeker_restclient.dao_implementation.mock import get_mockdata_url
from django.conf import settings


class File(object):
    def getURL(self, url, headers):
        return get_mockdata_url("spotseeker", "file", url, headers)


class Live(object):
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = self._get_pool()

        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENT_SPOTSEEKER_HOST,
                            url, headers=headers,
                            service_name='spotseeker')

    def _get_pool(self):
        return get_con_pool(settings.RESTCLIENT_SPOTSEEKER_HOST)
