"""
Contains DAO Cache implementations
"""
from spotseeker_restclient.mock_http import MockHTTP
from spotseeker_restclient.models import CacheEntry, CacheEntryTimed
from spotseeker_restclient.cache_manager import store_cache_entry
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, get_current_timezone


class NoCache(object):
    """
    This never caches anything.
    """
    def getCache(self, service, url, headers):
        return None

    def processResponse(self, service, url, response):
        pass


class TimedCache(object):
    """
    This is a base class for Cache implementations that cache for
    lengths of time.
    """
    def _response_from_cache(self, service, url, headers, max_age_in_seconds,
                             max_error_age=60 * 5):

        # If max_age_in_seconds is 0,
        # make sure we don't get a hit from this same second.
        if not max_age_in_seconds:
            return None
        now = make_aware(datetime.now(), get_current_timezone())
        time_limit = now - timedelta(seconds=max_age_in_seconds)

        query = CacheEntryTimed.objects.filter(service=service,
                                               url=url,
                                               time_saved__gte=time_limit)

        if len(query):
            hit = query[0]

            if hit.status != 200 and (
                    now - timedelta(seconds=max_error_age) > hit.time_saved):
                return None

            response = MockHTTP()
            response.status = hit.status
            response.data = hit.content
            response.headers = hit.getHeaders()

            return {
                "response": response,
            }
        return None

    def _process_response(self, service, url, response,
                          overwrite_success_with_error_at=60 * 60 * 8):
        now = make_aware(datetime.now(), get_current_timezone())
        query = CacheEntryTimed.objects.filter(service=service,
                                               url=url)

        cache_entry = None
        if len(query):
            cache_entry = query[0]
        else:
            cache_entry = CacheEntryTimed()

        if response.status != 200:
            # Only override a successful cache entry with an error if the
            # Successful entry is older than 8 hours - MUWM-509
            if cache_entry.id is not None and cache_entry.status == 200:
                save_delta = now - cache_entry.time_saved
                extended_cache_delta = timedelta(
                    seconds=overwrite_success_with_error_at)

                if save_delta < extended_cache_delta:
                    response = MockHTTP()
                    response.status = cache_entry.status
                    response.data = cache_entry.content
                    return {"response": response}

        cache_entry.service = service
        cache_entry.url = url
        cache_entry.status = response.status
        cache_entry.content = response.data

        # This extra step is needed w/ Live resources because
        # HTTPHeaderDict isn't serializable.
        header_data = {}
        for header in response.headers:
            header_data[header] = response.getheader(header)

        cache_entry.headers = header_data
        cache_entry.time_saved = now

        try:
            store_cache_entry(cache_entry)
        except Exception as ex:
            # If someone beat us in to saving a cache entry, that's ok.
            # We just need a very recent entry.
            return

        return


class TimeSimpleCache(TimedCache):
    """
    This caches all URLs for 60 seconds.  Used for testing.
    """
    def getCache(self, service, url, headers):
        return self._response_from_cache(service, url, headers, 60)

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)


class FourHourCache(TimedCache):
    """
    This caches all URLs for 4 hours.  Provides a basic way to cache
    cache resources that don't give a useful expires header, but you don't
    want to make a server round trip to validate an etag for.
    """
    def getCache(self, service, url, headers):
        return self._response_from_cache(service, url, headers,  60 * 60 * 4)

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)


class ETagCache(object):
    """
    This caches objects just based on ETags.
    """
    def getCache(self, service, url, headers):
        now = make_aware(datetime.now(), get_current_timezone())
        time_limit = now - timedelta(seconds=60)

        query = CacheEntry.objects.filter(service=service,
                                          url=url)

        if len(query):
            hit = query[0]

            response = MockHTTP()
            response.status = hit.status
            response.data = hit.content

            hit_headers = hit.getHeaders()

            if "ETag" in hit_headers:
                headers["If-None-Match"] = hit_headers["ETag"]

        return None

    def processResponse(self, service, url, response):
        query = CacheEntryTimed.objects.filter(service=service,
                                               url=url)

        cache_entry = CacheEntryTimed()
        if len(query):
            cache_entry = query[0]

        if response.status == 304:
            if cache_entry is None:
                raise Exception("304, but no content??")

            response = MockHTTP()
            response.status = cache_entry.status
            response.data = cache_entry.content
            response.headers = cache_entry.headers
            return {"response": response}
        else:
            now = make_aware(datetime.now(), get_current_timezone())
            cache_entry.service = service
            cache_entry.url = url
            cache_entry.status = response.status
            cache_entry.content = response.data

            cache_entry.headers = response.headers
            cache_entry.time_saved = now
            store_cache_entry(cache_entry)

        return
