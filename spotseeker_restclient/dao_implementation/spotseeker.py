from importlib import import_module
from spotseeker_restclient.dao_implementation.live import get_live_url
from spotseeker_restclient.dao_implementation.mock import get_mockdata_url
from django.conf import settings


class File(object):
    def getURL(self, url, headers):
        return get_mockdata_url("spotseeker", "file", url, headers)


class Live(object):

    def getURL(self, url, headers):

        return get_live_url('GET',
                            settings.SPOTSEEKER_HOST,
                            url, headers=headers)

    def putURL(self, url, headers, body):
        return get_live_url('PUT',
                            settings.SPOTSEEKER_HOST,
                            url,
                            headers=headers,
                            body=body)

    def deleteURL(self, url, headers, body):
        return get_live_url('DELETE',
                            settings.SPOTSEEKER_HOST,
                            url,
                            headers=headers,
                            body=body)
