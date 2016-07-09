"""
Provides access to the http connection pools and
connections for live data from a web service

"""
import oauth2

from django.conf import settings


def get_live_url(method,
                 host,
                 url,
                 headers,
                 body=''):
    """
    Return a connection from the pool and perform an HTTP request.
    :param con_pool:
        is the http connection pool associated with the service
    :param method:
        HTTP request method (such as GET, POST, PUT, etc.)
    :param host:
        the url of the server host.
    :param headers:
        headers to include with the request
    :param body:
        the POST, PUT body of the request
    """
    consumer = oauth2.Consumer(key=settings.SPOTSEEKER_OAUTH_KEY,
                               secret=settings.SPOTSEEKER_OAUTH_SECRET)
    client = oauth2.Client(consumer)
    url = host + url

    resp, content = client.request(url,
                                   method=method,
                                   body=body,
                                   headers=headers)
    return (resp, content)
