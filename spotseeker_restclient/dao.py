from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import *
from spotseeker_restclient.cache_implementation import NoCache
from spotseeker_restclient.dao_implementation.spotseeker import File \
    as SpotseekerFile


class DAO_BASE(object):
    def _getModule(self, settings_key, default_class):
        if hasattr(settings, settings_key):
            # This is all taken from django's static file finder
            module, attr = getattr(settings, settings_key).rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                config_module = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                           '"%s" class' % (module, attr))
            return config_module()
        else:
            return default_class()


class MY_DAO(DAO_BASE):
    def _getCache(self):
        return self._getModule('DAO_CACHE_CLASS', NoCache)

    def _getURL(self, service, url, headers):
        dao = self._getDAO()
        cache = self._getCache()
        cache_response = cache.getCache(service, url, headers)
        if cache_response is not None:
            if "response" in cache_response:
                return cache_response["response"]
            if "headers" in cache_response:
                headers = cache_response["headers"]

        response = dao.getURL(url, headers)

        cache_post_response = cache.processResponse(service, url, response)

        if cache_post_response is not None:
            if "response" in cache_post_response:
                return cache_post_response["response"]

        return response

    def _postURL(self, service, url, headers, body=None):
        dao = self._getDAO()
        response = dao.postURL(url, headers, body)
        return response

    def _deleteURL(self, service, url, headers):
        dao = self._getDAO()
        response = dao.deleteURL(url, headers)
        return response

    def _putURL(self, service, url, headers, body=None):
        dao = self._getDAO()
        response = dao.putURL(url, headers, body)
        return response


class SPOTSEEKER_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('spotseeker', url, headers)

    def _getDAO(self):
        return self._getModule('SPOTSEEKER_DAO_CLASS',
                               SpotseekerFile)
